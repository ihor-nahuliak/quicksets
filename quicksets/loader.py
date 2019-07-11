# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import inspect
import importlib


class Settings:
    """Loads settings by name from ENV "SETTINGS" variable;
    imports the module and tries to create instance
    of the last imported class as protected _settings object.

    WARNING! If you have more than one public class in your module
             it takes the last one sorting available classes by alphabet.
             Please, use __all__ magic variable to not confuse.

    :param str module_name: name of the module that contains settings class
    """
    env_variable = 'SETTINGS'  # this const can be overridden in you own class

    def __init__(self, module_name=None):
        self.__module_name = module_name
        self.__settings = None

    def _load(self):
        """It returns the last public class instance available
        in the module which name is read from _module_name property.
        If the imported module contains __all__ magic variable,
        it lookups in that iterator only to find the config class.
        It ignores any protected and public classes which names
        started from "_" symbol.

        :return: an instance of the config class
                 available in the module.
        """
        settings_class = None
        try:
            settings_module = importlib.import_module(self._module_name)
        except ImportError:
            raise ImportError(
                'Can not import settings module "%s"' % self._module_name)

        for attr_name, attr in inspect.getmembers(settings_module):
            if (hasattr(settings_module, '__all__') and
                    attr_name not in settings_module.__all__):
                # lookup public module's attributes only
                continue
            if attr_name.startswith('_') or not inspect.isclass(attr):
                # lookup public classes only
                continue
            # do not break, it needs to take the last one
            settings_class = attr

        if not settings_class:
            raise ImportError('Can not find any config class '
                              'in module "%s"' % self._module_name)

        return settings_class()

    @property
    def _module_name(self):
        """Lazy property."""
        if not self.__module_name:
            self.__module_name = os.environ.get(self.env_variable, None)
            if not self.__module_name:
                raise EnvironmentError(
                    'ENV "{0}" variable was not set. '
                    'Please setup it like: '
                    '`export {0}="myapp.settings.production"` '
                    'or simple use Settings class with '
                    'module_name argument.'.format(self.env_variable)
                )
        return self.__module_name

    @property
    def _settings(self):
        """Lazy property."""
        if not self.__settings:
            self.__settings = self._load()  # lazy
        return self.__settings

    def __getattr__(self, name):
        return getattr(self._settings, name)
