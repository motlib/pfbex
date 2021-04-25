'''Utility to dump all TR-064 service actions of a FritzBox including their
values.'''

import csv

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
        print(f'Skipping {service.name}:{action.name} because of in args.')
        return

    if not outargs:
        print(f'Skipping {service.name}:{action.name} because of no out args.')
        return

    print(f'Retrieving {service.name}:{action.name}.')

    try:
        res = conn.call_action(service.name, action.name)

        if not res:
            return
    except:
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

    filename = 'dump.csv'

    settings = EnvSettingsResolver(SETTINGS_DESC)

    conn = fc.FritzConnection(
        address=settings.FRITZ_HOST,
        user=settings.FRITZ_USER,
        password=settings.FRITZ_PASS)

    with open(filename, 'w', newline='') as fhdl:
        writer = csv.writer(fhdl)

        writer.writerow(['Service', 'Action', 'Attribute', 'Value'])

        for row in process_all(conn):
            writer.writerow(row)

    print(f'Results written to {filename}.')

if __name__ == '__main__':
    main()
