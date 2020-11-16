'''FritzBox exporter implementation'''

from datetime import datetime

import fritzconnection as fc
from prometheus_client import Summary
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily

from .logging import logger


MAX_FAILS = 3

# Minimum time before the cache is updated again with new data from the FritzBox
MIN_UPDATE_TIME = 30


class FritzBoxExporter(): # pylint: disable=too-few-public-methods
    '''FrizBox exporter implementation retrieving metrics from a FritzBox by
    TR-064. This is used by the prometheus client implementation to publish the
    metrics.'''

    config_desc = {
        'FRITZ_HOST': {
            'default': 'fritz.box',
            'help': 'Hostname of the FritzBox to query.'
        },
        'FRITZ_USER': {
            'required': True,
            'help': 'Username to log in to the FritzBox to retrieve metrics'
        },
        'FRITZ_PASS': {
            'required': True,
            'help': 'Password to log in to the FritzBox to retrieve metrics'
        },
        'CACHE_TIME': {
            'default': 30,
            'help': (
                'Time to keep results in an internal cache before querying the '
                'FritzBox again')
        },
    }

    request_tm = Summary(
        'fb_exporter_request',
        'Time and count for each request to the FritzBox')

    def __init__(self, settings, metrics):
        self.conn = fc.FritzConnection(
            address=settings.FRITZ_HOST,
            user=settings.FRITZ_USER,
            password=settings.FRITZ_PASS)

        self._settings = settings
        self._cfg = metrics

        for item in self._cfg.values():
            item['fails'] = 0

        self._serial = 'n/a'

        self._data = {}
        self._last_clear_time = datetime.now()


    def _reset_request_cache(self):
        '''Clear the request result cache.'''

        now = datetime.now()
        if (now - self._last_clear_time).seconds > MIN_UPDATE_TIME:
            logger.debug('Clearing request cache.')
            self._data.clear()

            self._last_clear_time = now


    @request_tm.time()
    def _call_action(self, service, action):
        '''Call an TR-64 service action and return the result.

        If the call fails, returns None. The result (both valid results and
        errors) are stored in the cache for the current scrape.

        '''

        key = f'{service}:{action}'

        # Return result from cache if available
        if key in self._data:
            return self._data[key]

        # Retrieve service information
        try:
            res = self.conn.call_action(service, action)
        except Exception as ex: # pylint: disable=broad-except
            res = None

            logger.debug(
                f'Failed to call service action {service}:{action}: {ex}')

        self._data[key] = res

        return res


    def _collect_device_info(self):
        '''Provide a Prometheus metric with the device information (model name,
        software version and serial number).

        At the same time, this function stores the FritzBox serial number for
        later use in all other metrics.

        '''

        res = self._call_action('DeviceInfo1', 'GetInfo')

        if not res:
            self._serial = 'n/a'
            return

        self._serial = res['NewSerialNumber']

        label_names = ['ModelName', 'SoftwareVersion', 'Serial']

        met = GaugeMetricFamily(
            'fritzbox_info',
            'FritzBox device information',
            labels=label_names)

        label_values = [
            res['NewModelName'],
            res['NewSoftwareVersion'],
            res['NewSerialNumber']
        ]

        met.add_metric(label_values, 1.0)

        yield met


    def _get_metric_label_names(self, metric): # pylint: disable=no-self-use
        '''Calculate label names for a Prometheus metric'''

        m_labels = set()

        for item in metric['items']:
            labels = item.get('labels', {})
            m_labels.update(labels.keys())

        label_names = ['serial']
        label_names.extend(m_labels)

        return label_names


    def _collect_metric_item(self, item, label_names):
        '''Collect metric data for one Prometheus metric instance (i.e. one assignment
        of label values).'''

        labels = item.get('labels', {})
        labels.update({'serial': self._serial})

        label_values = [labels[name] for name in label_names]

        service = item['service']
        action = item['action']
        attr = item['attr']

        service_data = self._call_action(service, action)

        if not service_data:
            logger.debug(f"No data available for '{service}:{action}'.")
            return None

        if not attr in service_data:
            # data has been retrieved, but attribute is missing
            logger.warning(
                f"Attribute '{attr}' not found in data of '{service}:{action}'.")
            logger.debug(f'Available data: {service_data}')
            return None

        fct = item.get('fct', lambda x: x)
        value = service_data[attr]
        try:
            value = fct(value)
            value = float(value)
        except Exception as ex: # pylint: disable=broad-except
            logger.warning(
                f"Could not convert value '{attr}={value}' for "
                f"'{service}:{action}: {ex}")

        return (label_values, value)


    def _collect_metric(self, metric_name, metric):
        '''Collect data for one Prometheus metric.'''

        label_names = self._get_metric_label_names(metric)
        metric_type = metric.get('type', 'gauge')

        if metric_type == 'counter':
            met = CounterMetricFamily(
                metric_name,
                metric['doc'],
                labels=label_names)
        elif metric_type == 'gauge':
            met = GaugeMetricFamily(
                metric_name,
                metric['doc'],
                labels=label_names)
        else:
            logger.error(
                f"Invalid metric type definition '{metric_type}' for metric "
                f"'{metric_name}'. Using default type 'gauge'.")

            met = GaugeMetricFamily(
                metric_name,
                metric['doc'],
                labels=label_names)

        # Calculate the metric labels and values
        item_count = 0
        for item in metric['items']:
            result = self._collect_metric_item(item, label_names)

            if result is None:
                continue

            item_count += 1

            (label_values, value) = result

            met.add_metric(label_values, value)

        if item_count > 0:
            yield met
        else:
            logger.debug(
                f"Dropping metric '{metric_name}', because no data was added.")


    def _collect_metrics(self):
        '''Loop over all metrics configurations and collect the data.'''

        for name, metric in self._cfg.items():
            yield from self._collect_metric(name, metric)


    def collect(self):
        '''Collect all metrics.

        This function is called by the Prometheus client implementation..

        '''

        # Clear the cache, so that no old data is reported.
        self._reset_request_cache()

        # Fetch device info about the FritzBox. This function has to be called first to
        # set the FritzBox serial number for the following metrics.
        yield from self._collect_device_info()

        # Fetch data from FritzBox and generate metrics
        yield from self._collect_metrics()
