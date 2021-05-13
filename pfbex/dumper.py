'''Utility to dump all TR-064 service actions of a FritzBox including their
values.'''

import csv
import logging


def _process_action(conn, service, action):
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
                'No response returned when accessing '
                f'{service.name}:{action.name}')
            return
    except Exception as ex: # pylint: disable=broad-except
        logging.exception(
            f'Failed to access {service.name}:{action.name}: {ex}')
        return

    for attr, val in res.items():
        yield [service.name, action.name, attr, val]


def _process_service(conn, service):
    '''Handle a service'''

    for action in service.actions.values():
        yield from _process_action(conn, service, action)


def _process_all(conn):
    '''Handle all services'''

    for service in conn.services.values():
        yield from _process_service(conn, service)


def dump_services(output_file, conn, dump_data):
    '''Dump all services and actions returning information (no input args, at
    least one output arg) to a CSV file.

    :param output_file: The file to write the results to.
    :param conn: The FritzConnection instance
    :param dump_data: Boolean, if set to true, the dump will contain the actual
      values returned from the FritzBox. This might contain sensitive
      information.

    '''

    results = []
    results.extend(_process_all(conn))
    results.sort(key=lambda e: (e[0], e[1], e[2]))

    with open(output_file, 'w', newline='') as fhdl:
        writer = csv.writer(fhdl)

        writer.writerow(['Service', 'Action', 'Attribute', 'Value'])

        for row in results:
            if not dump_data:
                row = row[0:3]

            writer.writerow(row)

    logging.info(f'Wrote {len(results)} services / actions to {output_file}.')
