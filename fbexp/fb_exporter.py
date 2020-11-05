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

import fritzconnection as fc
from prometheus_client.core import (
    GaugeMetricFamily, CounterMetricFamily, REGISTRY)
from prometheus_client import start_http_server

from .metrics_config import METRICS_CFG


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


MAX_FAILS = 3

class FritzBoxExporter():

    def __init__(self, host, user, passwd, cfg):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.conn = fc.FritzConnection(
            address=self.host,
            user=self.user,
            password=self.passwd)

        self._cfg = cfg

        for item in self._cfg:
            item['fails'] = 0


        self._retrieve_serial_no()


    def _call_action(self, service, action):
        '''Call an TR-64 service action and return the result. If the call fails,
        returns None.'''

        try:
            res = self.conn.call_action(service, action)
        except:
            res = None

        return res


    def _retrieve_serial_no(self):
        '''Retrieve the serial number from the fritzbox.'''

        res = self._call_action('DeviceInfo1', 'GetInfo')
        if not res:
            self._serial = 'n/a'
        else:
            self._serial = res['NewSerialNumber']


    def _collect_device_info(self):
        '''Manually provide a prometheus metric with the device information model name,
        software version and serial number.'''

        res = self._call_action('DeviceInfo1', 'GetInfo')

        if not res:
            return

        met = GaugeMetricFamily(
            'fritzbox_info',
            'FritzBox device information',
            labels=['ModelName', 'SoftwareVersion', 'Serial'])
        met.add_metric(
            [
                res['NewModelName'],
                res['NewSoftwareVersion'],
                res['NewSerialNumber']
            ],
            1.0)

        yield met


    def _collect_metric(self, cfg):
        '''Collect data from one service / action config.'''

        service = cfg['service']
        action = cfg['action']
        metrics = cfg['metrics']
        fails = cfg.get('fails', 0)

        # If we had multiple failures to retrieve TR-64 data, we will skip this
        # config.
        if fails > MAX_FAILS:
            return

        logger.debug(f"Retrieving data from {service}:{action}")

        res = self._call_action(service, action)
        if not res:
            logger.warning(f'Failed to retrieve data from service {service}:{action} (repeated {fails}).')

            cfg['fails'] = fails + 1

            if cfg['fails'] >= MAX_FAILS:
                logging.warning(f'Disabled further requests to {service}:{action}.')

            return

        for metric in metrics:
            key = metric['key']
            if key not in res:
                logger.warning(f'Key {key} not in TR-64 result data of {service}:{action}.')
                continue

            met = GaugeMetricFamily(
                metric['metric'],
                metric['doc'],
                labels=['Serial'])

            value = res[metric['key']]
            if 'fct' in metric:
                value = metric['fct'](value)

            met.add_metric([self._serial], value)

            yield met


    def collect(self):
        yield from self._collect_device_info()

        for cfg in self._cfg:
            yield from self._collect_metric(cfg)
