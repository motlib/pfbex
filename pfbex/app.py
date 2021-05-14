'''Application main function'''

from datetime import datetime
import os
import signal
import sys
import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
import fritzconnection as fc


from .dumper import dump_services
from .exporter import FritzBoxExporter
from .metrics_config import load_all_metrics_configs
from .logging import setup_logging, logger
from .metadata import APP_NAME, APP_VERSION
from .settings import EnvSettingsResolver
from .settings_desc import SETTINGS_DESC


def sig_term(signum, frame):
    '''Handler function for SIGTERM to shut down this process in a docker
    container.'''

    del signum
    del frame

    logger.info('Terminating on SIGTERM. Bye!')

    # We do not need to tidy up anything. So just exit.
    sys.exit(0)


def main():
    '''Main method initializing the application and starting the exporter.'''

    # Register the handler for the SIGTERM signal to exit app when container is
    # shutting down.
    signal.signal(signal.SIGTERM, sig_term)

    settings = EnvSettingsResolver(SETTINGS_DESC)

    setup_logging(level=settings.LOGLEVEL)

    logger.info(f'Starting {APP_NAME} version {APP_VERSION}.')

    logger.debug(
        'Dumping effective application settings\n' + settings.to_table())

    conn = fc.FritzConnection(
        address=settings.FRITZ_HOST,
        user=settings.FRITZ_USER,
        password=settings.FRITZ_PASS)

    if settings.DUMP_SERVICES:
        dtm = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'dump_{dtm}.csv'
        output_file = os.path.join(
            os.path.dirname(__file__), '..', 'output', file_name)

        logger.info(f'Dumping FritzBox services to {file_name}')
        dump_services(
            output_file=output_file,
            conn=conn,
            dump_data=(settings.DUMP_DATA == '1'))

        logger.info(
            f"Terminating after dumping serices to '{file_name}'. If you want "
            'to use normal exporter functionality, please unset DUMP_SERICES '
            'environment variable.')

        sys.exit(0)

    # Create exporter instance and register it with the prometheus client lib
    metrics = load_all_metrics_configs(settings.METRICS_PATH)
    exporter = FritzBoxExporter(conn, metrics)
    REGISTRY.register(exporter)

    # Start up the server to expose the metrics.
    logger.info(f'Web server is listening on port {settings.HTTP_PORT}.')
    start_http_server(settings.HTTP_PORT)

    # Now we wait for incoming HTTP requests
    while True:
        time.sleep(10000)
