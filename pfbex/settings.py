'''Settings handling'''

from abc import ABC, abstractmethod
import os

from tabulate import tabulate


class SettingsException(Exception):
    '''Base class for all settings related exceptions.'''


class SettingsResolver(ABC):
    '''Abstract base class implementing the general functionality of a settings
    resolver.'''

    def __init__(self, *descs):
        '''Initialize the settings resolver. Multiple descriptors can be passed in. They
        will be merged into one descriptor. If descriptor entries are defined
        multiple times, an exception is raised.

        '''

        self._desc = {}

        for desc in descs:
            self.add_descriptor(desc)


    def add_descriptor(self, desc):
        '''Add another settings descriptor to the resolver.'''

        for item in desc:
            if item in self._desc:
                raise SettingsException(
                    f"The descriptor item '{item}' is redefined.")
            self._desc[item] = desc[item]


    def get(self, name):
        '''Retrieve a settings value.'''

        if name not in self._desc:
            raise SettingsException(
                f"Settings name '{name}' is not specified in the config "
                "descriptor.")

        if self.is_configured(name):
            return self.get_configured_value(name)

        if self.is_required(name):
            raise SettingsException(
                f"Required setting '{name}' is not configured.")

        return self.get_default(name)


    def __getattr__(self, name):
        '''Retrieve a settings value by attribute access.'''
        return self.get(name)


    @abstractmethod
    def is_configured(self, name):
        '''Return true if the key is explicitly configured.'''


    @abstractmethod
    def get_configured_value(self, name):
        '''Return the explicitly configured value for this key.'''


    def get_help(self, name):
        '''Return the help text of a setting.'''

        return self._desc[name].get('help', '')


    def get_default(self, name):
        '''Return the default value of a setting.'''

        return self._desc[name].get('default', None)


    def is_required(self, name):
        '''Returns true if a setting is required to be configured.'''

        return self._desc[name].get('required', False)


    def to_table(self):
        '''Format all settings as a table formatted for printing to the console.'''

        headers = ['Name', 'Value', 'Configured', 'Default', 'Type', 'Help']
        rows = []

        for name in self._desc:
            eff_val = self.get(name)

            rows.append([
                name,
                eff_val,
                'yes' if self.is_configured(name) else 'no',
                self.get_default(name),
                eff_val.__class__.__name__,
                self.get_help(name)
            ])

        return tabulate(rows, headers=headers, tablefmt='psql', stralign='left')



class EnvSettingsResolver(SettingsResolver):
    '''Settings resolver implementation retrieving settings from environment
    variables.'''

    def is_configured(self, name):
        return name in os.environ


    def get_configured_value(self, name):
        return os.environ[name]
