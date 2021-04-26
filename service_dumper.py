'''Utility to dump all TR-064 service actions of a FritzBox including their
values.'''

import csv
import logging

import fritzconnection as fc

from pfbex.settings import EnvSettingsResolver


SETTINGS_DESC = {
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
}


def process_action(conn, service, action):
    '''Handle one action'''

    args = action.arguments.values()

    inargs = sum(1 for arg in args if arg.direction == 'in')
    outargs = sum(1 for arg in args if arg.direction == 'out')

    if inargs:
        logging.info(
            f'Skipping {service.name}:{action.name} because it has input args.')
        return

    if not outargs:
        logging.info(
            f'Skipping {service.name}:{action.name} because it has no output '
            'args.')
        return

    logging.debug(f'Retrieving {service.name}:{action.name}.')

    try:
        res = conn.call_action(service.name, action.name)

        if not res:
            logging.warning(
                f'No response returned when accessing '
                '{service.name}:{action.name}')
            return
    except Exception as ex:
        logging.exception(
            f'Failed to access {service.name}:{action.name}: {ex}')
        return

    for attr, val in res.items():
        yield [service.name, action.name, attr, val]



def process_service(conn, service):
    '''Handle a service'''
    for action in service.actions.values():
        yield from process_action(conn, service, action)


def process_all(conn):
    '''Handle all services'''

    for service_name, service in conn.services.items():
        yield from process_service(conn, service)


def main():
    '''Application entry point.'''

    logging.basicConfig(
        format='%(asctime)-15s %(levelname)s: %(message)s',
        level=logging.INFO)

    filename = 'dump.csv'

    settings = EnvSettingsResolver(SETTINGS_DESC)

    conn = fc.FritzConnection(
        address=settings.FRITZ_HOST,
        user=settings.FRITZ_USER,
        password=settings.FRITZ_PASS)


    results = []
    results.extend(process_all(conn))
    results.sort(key=lambda e: (e[0], e[1],))

    with open(filename, 'w', newline='') as fhdl:
        writer = csv.writer(fhdl)

        writer.writerow(['Service', 'Action', 'Attribute', 'Value'])

        for row in results:
            writer.writerow(row)

    logging.info(f'Wrote {len(results)} services / actions to {filename}.')

if __name__ == '__main__':
    main()
