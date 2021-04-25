'''Application main function'''

import signal
import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from .exporter import FritzBoxExporter
from .metrics_config import load_all_metrics_configs
from .logging import setup_logging, logger
from .metadata import APP_NAME, APP_VERSION
from .settings import EnvSettingsResolver


APP_SETTINGS_DESC = {
    'HTTP_PORT': {
        'default': 8765,
        'help': 'Port for the integrated http web server'
    },
    'LOGLEVEL': {
        'default': 'info',
        'help': "Log level, one of 'debug', 'info', 'warning' or 'error'"
    },
    'METRICS_PATH': {
        'default': './conf',
        'help': 'Path to the metrics configuration files.'
    }
}


def sig_term():
    '''Handler function for SIGTERM to shut down this process in a docker
    container.'''

    # We do not need to tidy up anything. So just exit.
    sys.exit(0)


def main():
    '''Main method initializing the application and starting the exporter.'''

    signal.signal(signal.SIGTERM, sig_term)

    settings = EnvSettingsResolver(
        FritzBoxExporter.config_desc,
        APP_SETTINGS_DESC)

    level = settings.LOGLEVEL
    setup_logging(level)

    logger.info(f'Starting {APP_NAME} version {APP_VERSION}.')
    logger.info(f"Log level is set to '{level}'.")

    logger.debug(
        'Dumping effective application settings\n' + settings.to_table())

    # Create exporter instance and register it with the prometheus client lib
    cfg = load_all_metrics_configs(settings.METRICS_PATH)
    exporter = FritzBoxExporter(settings, cfg)
    REGISTRY.register(exporter)

    # Start up the server to expose the metrics.
    logger.info(f'Web server is listening on port {settings.HTTP_PORT}.')
    start_http_server(settings.HTTP_PORT)

    # Now we wait for incoming HTTP requests
    while True:
        time.sleep(10000)
