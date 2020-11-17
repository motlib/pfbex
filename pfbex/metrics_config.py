'''Loading of metrics configuration files.'''

import glob
import os

import yaml

from .logging import logger


def load_all_metrics_configs(directory):
    '''Load all metric configuration files (extension must by .yml) from the
    specified directory.'''


    files = glob.glob(os.path.join(directory, '*.yml'))

    cfg = {}

    for filename in files:
        logger.debug(f"Loading metric config from '{filename}'.")

        file_cfg = _load_metrics_config(filename)

        for key in file_cfg:
            if key in cfg:
                raise Exception(
                    f"Duplicate definition of metric '{key}' in '{filename}'.")

        cfg.update(file_cfg)

        logger.info(f"Loaded {len(file_cfg)} metrics from '{filename}'.")

    return cfg


def _load_metrics_config(filename):
    '''Load the specified metrics configuration file.'''

    with open(filename, 'r') as fhdl:
        data = yaml.load(fhdl, Loader=yaml.SafeLoader)

    for metric in data.values():
        for item in metric['items']:
            if 'fct' in item:
                item['fct'] = eval(item['fct']) # pylint: disable=eval-used

    return data
