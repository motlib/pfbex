# Copyright 2019 Patrick Dreker <patrick@dreker.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import logging.config
import os
import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from .fb_exporter import FritzBoxExporter
from .metrics_config import METRICS_CFG


def main():
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

    fb_exporter = FritzBoxExporter(
        os.getenv('FRITZ_HOST', 'fritz.box'),
        os.getenv('FRITZ_USER'),
        os.getenv('FRITZ_PASS'),
        METRICS_CFG)

    REGISTRY.register(fb_exporter)

    # Start up the server to expose the metrics.
    start_http_server(os.getenv('FRITZ_EXPORTER_PORT', 8765))
    while(True):
        time.sleep(10000)


if __name__ == '__main__':
    main()
