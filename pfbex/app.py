'''Application main function'''

import os
import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from .exporter import FritzBoxExporter
from .metrics_config import METRICS_CFG
from .logging import setup_logging, logger
from .metadata import APP_NAME, APP_VERSION


DEFAULT_HOST = 'fritz.box'
DEFAULT_PORT = '8765'
DEFAULT_LOGLEVEL = 'info'


def main():
    '''Main method initializing the application and starting the exporter.'''

    level = os.getenv('LOGLEVEL', DEFAULT_LOGLEVEL).upper()

    setup_logging(level)

    logger.info(f'Starting {APP_NAME} version {APP_VERSION}.')
    logger.info(f"Log level is set to '{level}'.")

    host = os.getenv('FRITZ_HOST', DEFAULT_HOST)
    user = os.getenv('FRITZ_USER', None)
    password = os.getenv('FRITZ_PASS', None)

    if (user is None) or (password is None):
        logger.error(
            'User and/or password to log in to FritzBox are not available. '
            'Please make sure to set FRITZ_USER and FRITZ_PASS environment '
            'variables correctly.')

        return 1

    exporter = FritzBoxExporter(
        host,
        user,
        password,
        METRICS_CFG)

    REGISTRY.register(exporter)

    # Start up the server to expose the metrics.
    port = int(os.getenv('FRITZ_EXPORTER_PORT', DEFAULT_PORT))
    logger.info(f'Web server is listening on port {port}.')

    start_http_server(port)

    while True:
        time.sleep(10000)