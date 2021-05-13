'''Logging-related functionality'''

import logging
import logging.config


logger = logging.getLogger('pfbex')


def setup_logging(level):
    '''Set up the logging output.'''

    logging.basicConfig(
        format='%(asctime)-15s %(levelname)s: %(message)s')

    logging.config.dictConfig({
        'version': 1,
        'loggers': {
            'pfbex': {
                'level': level.upper()
            }
        }
    })

    logger.info(f"Log level is set to '{level}'.")
