'''FritzBox collector implementation'''

import logging
import logging.config

import fritzconnection as fc
from prometheus_client import Summary
from prometheus_client.core import GaugeMetricFamily

from collections import defaultdict


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


MAX_FAILS = 3

class FritzBoxExporter(): # pylint: disable=too-few-public-methods
    '''FrizBox exporter implementation retrieving metrics from a FritzBox by
    TR-064. This is used by the prometheus client implementation to publish the
    metrics.'''

    collect_tm = Summary(
        'fb_exporter_collect',
        'Time and count of data collections from fritzbox')

    request_tm = Summary(
        'fb_exporter_request',
        'Time and count for each request to the FritzBox')

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



    @request_tm.time()
    def _call_action(self, service, action):
        '''Call an TR-64 service action and return the result. If the call fails,
        returns None.'''

        try:
            res = self.conn.call_action(service, action)
        except: # pylint: disable=bare-except
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


    @collect_tm.time()
    def _update_data(self, cfg):
        '''Collect all service identifiers from the configuration and fetch
        their data once.'''

        logger.debug('Updating service data from FritzBox')
        self._data = {}

        for metric in cfg:
            for item in metric['items']:

                key = item['service'] + ':' + item['action']

                if key in self._data:
                    # data for this service / action has already been fetched
                    continue

                logger.debug(f"Fetching data for '{key}'.")

                try:
                    self._data[key] = self._call_action(item['service'], item['action'])
                except Exception as ex:
                    logging.warning(f"Failed to fetch data for '{key}': {ex}")
                    self._data[key] = None


    def _get_metrics(self, cfg):
        '''Loop over all metrics configurations'''

        for metric in cfg:

            # Calculate label names for this metric
            m_labels = set()
            for item in metric['items']:
                labels = item.get('labels', {})
                m_labels.update(labels.keys())

                label_names = list(m_labels)

            met = GaugeMetricFamily(
                metric['metric'],
                metric['doc'],
                labels=['serial'] + label_names)

            # Calculate the metric labels and values
            for item in metric['items']:
                label_values = [self._serial]
                label_values += [item['labels'][name] for name in label_names]

                service_key = item['service'] + ':' + item['action']
                attr = item['attr']

                s_data = self._data.get(service_key, None)

                if not s_data:
                    # no data has been retrieved
                    logger.debug(f"No data available for '{service_key}'.")
                    continue

                if not attr in s_data:
                    # data has been retrieved, but attribute is missing
                    logger.warning(
                        f"Attribute '{attr}' not found in data of "
                        f"'{service_key}'.")
                    logger.debug(f'Available data: {s_data}')
                    continue

                fct = item.get('fct', lambda x: x)
                in_val = s_data[attr]
                try:

                    value = float(fct(s_data[attr]))
                except Exception as ex:
                    logger.warning(
                        f"Could not convert value '{attr}={in_val}' for "
                        f"'{service_key}: {ex}")

                met.add_metric(label_values, value)

            yield met


    def collect(self):
        '''Collect all metrics. This is called by the prometheus client
        implementation..'''

        # fetch info about the FritzBox
        yield from self._collect_device_info()

        # Fetch data from FritzBox and generate metrics
        self._update_data(self._cfg)
        yield from self._get_metrics(self._cfg)
