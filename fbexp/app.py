'''Application main function'''

import logging
import logging.config
import os
import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from .fb_exporter import FritzBoxExporter
from .metrics_config import METRICS_CFG

FRITZ_HOST_DEFAULT = 'fritz.box'
FRITZ_EXPORTER_PORT_DEFAULT = '8765'


def setup_logging():
    '''Set up the logging output.'''

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s %(levelname)s: %(message)s')

    logging.config.dictConfig({
        'version': 1,
        'loggers': {
            'fbexp': {
                'level': logging.DEBUG
            }
        }
    })


def main():
    '''Main method initializing the application and starting the exporter.'''

    setup_logging()

    fb_exporter = FritzBoxExporter(
        os.getenv('FRITZ_HOST', 'fritz.box'),
        os.getenv('FRITZ_USER'),
        os.getenv('FRITZ_PASS'),
        METRICS_CFG)

    REGISTRY.register(fb_exporter)

    # Start up the server to expose the metrics.
    port = int(os.getenv('FRITZ_EXPORTER_PORT', FRITZ_EXPORTER_PORT_DEFAULT))
    start_http_server(port)

    while True:
        time.sleep(10000)


if __name__ == '__main__':
    main()
