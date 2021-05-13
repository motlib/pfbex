'''Settings descriptor'''

SETTINGS_DESC = {
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
    },
    'DUMP_SERVICES': {
        'default': 0,
        'help': 'Set to 1 to dump service information of the FritzBox at startup.'
    },
    'DUMP_DATA': {
        'default': '0',
        'help': (
            'Set to 1 to dump data with services. This might dump sensitive'
            'information.')
    },
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
            'Time in seconds to keep results in the internal cache before '
            'querying the FritzBox again')
    },
}
