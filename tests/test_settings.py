# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

try:
    from unittest import mock
except ImportError:
    import mock  # python 2 compatibility

from quicksets import Settings


class TestCase(unittest.TestCase):

    def test_load_default_settings(self):
        settings = Settings('tests.settings.default')

        self.assertEqual(settings._settings.__class__.__name__,
                         'DefaultConfig')

    @mock.patch('quicksets.loader.os')
    def test_load_settings_by_env_variable_default(self, m_os):
        m_os.environ.get.return_value = 'tests.settings.default'

        settings = Settings()

        self.assertEqual(settings._settings.__class__.__name__,
                         'DefaultConfig')

    def test_load_develop_settings(self):
        settings = Settings('tests.settings.develop')

        self.assertEqual(settings._settings.__class__.__name__,
                         'DevelopConfig')

    @mock.patch('quicksets.loader.os')
    def test_load_settings_by_env_variable_develop(self, m_os):
        m_os.environ.get.return_value = 'tests.settings.develop'

        settings = Settings()

        self.assertEqual(settings._settings.__class__.__name__,
                         'DevelopConfig')

    def test_load_testing_settings(self):
        settings = Settings('tests.settings.testing')

        self.assertEqual(settings._settings.__class__.__name__,
                         'TestingConfig')

    @mock.patch('quicksets.loader.os')
    def test_load_settings_by_env_variable_testing(self, m_os):
        m_os.environ.get.return_value = 'tests.settings.testing'

        settings = Settings()

        self.assertEqual(settings._settings.__class__.__name__,
                         'TestingConfig')

    def test_load_product_settings(self):
        settings = Settings('tests.settings.product')

        self.assertEqual(settings._settings.__class__.__name__,
                         'ProductConfig')

    @mock.patch('quicksets.loader.os')
    def test_load_settings_by_env_variable_product(self, m_os):
        m_os.environ.get.return_value = 'tests.settings.product'

        settings = Settings()

        self.assertEqual(settings._settings.__class__.__name__,
                         'ProductConfig')

    def test_public_attribute_access_is_proxied(self):
        settings = Settings('tests.settings.develop')

        self.assertEqual(settings.POSTGRESQL_HOST, 'localhost')

    def test_public_attribute_access_is_proxied_to_not_existed_attr(self):
        settings = Settings('tests.settings.default')

        with self.assertRaises(AttributeError) as err_ctx:
            # here we are trying to take an access to public
            # attribute that doesn't exist in the config
            _ = settings.UNKNOWN_ATTRIBUTE
            self.assertEqual(
                err_ctx.exception.args[0],
                "'DefaultConfig' object has no attribute 'UNKNOWN_ATTRIBUTE'"
            )

    def test_load_alphabetic_configs_settings(self):
        settings = Settings('tests.settings.two_alphabetic_configs')

        self.assertEqual(settings._settings.__class__.__name__, 'ConfigB')

    def test_load_not_alphabetic_configs_settings(self):
        settings = Settings('tests.settings.two_not_alphabetic_configs')

        self.assertEqual(settings._settings.__class__.__name__, 'ConfigB')

    def test_hidden_configs_are_not_loaded(self):
        settings = Settings('tests.settings.two_hidden_configs')

        self.assertEqual(settings._settings.__class__.__name__, 'ConfigC')

    def test_load_not_class_public_objects_settings(self):
        settings = Settings('tests.settings.not_class_public_objects')

        self.assertEqual(settings._settings.__class__.__name__, 'ConfigD')

    def test_load_not_public_configs_settings(self):
        settings = Settings('tests.settings.two_not_public_configs')

        self.assertEqual(settings._settings.__class__.__name__, 'ConfigC')

    def test_load_no_class_empty_config_settings(self):
        settings = Settings('tests.settings.no_class_empty_config')

        with self.assertRaises(ImportError) as err_ctx:
            # here we take an access to the lazy object that can't be loaded
            _ = settings._settings
            self.assertEqual(
                err_ctx.exception.args[0],
                'Can not find any config class '
                'in module "%s"' % 'tests.settings.no_class_empty_config'
            )

    def test_load_config_module_that_does_not_exist(self):
        settings = Settings('tests.settings.does_not_exist')

        with self.assertRaises(ImportError) as err_ctx:
            # here we take an access to the lazy object that can't be loaded
            _ = settings._settings
            self.assertEqual(
                err_ctx.exception.args[0],
                'Can not import settings module "%s"' %
                'tests.settings.does_not_exist'
            )

    @mock.patch('quicksets.loader.Settings._load')
    def test_settings_property_doesnt_call_load_method_early(self, m_load):
        m_load.return_value.TEST_VALUE = 123

        settings = Settings('tests.settings.xyz')

        # private __settings object was not loaded
        self.assertIsNone(settings._Settings__settings)
        # lazy loader must not be called early
        m_load.assert_not_called()

    @mock.patch('quicksets.loader.Settings._load')
    def test_settings_lazy_property_calls_load_method_one_time(self, m_load):
        m_load.return_value.TEST_VALUE = 123

        settings = Settings('tests.settings.xyz')
        for _ in range(0, 2):
            # here we twice take an access to the lazy object
            self.assertEqual(settings._settings.TEST_VALUE, 123)

        # private __settings object was loaded
        self.assertIsNotNone(settings._Settings__settings)
        # lazy loader must be called just one time
        m_load.assert_called_once_with()

    @mock.patch('quicksets.loader.os')
    def test_module_name_property_doesnt_call_env_get_method_early(self, m_os):
        m_os.environ.get.return_value = 'tests.settings.xyz'

        settings = Settings()

        # private __module_name object was not loaded
        self.assertIsNone(settings._Settings__module_name)
        # os.env.get method must not be called early
        m_os.environ.get.assert_not_called()

    @mock.patch('quicksets.loader.os')
    def test_module_name_property_calls_env_get_method_one_time(self, m_os):
        m_os.environ.get.return_value = 'tests.settings.xyz'

        settings = Settings()
        for _ in range(0, 2):
            # here we twice take an access to the lazy object
            self.assertEqual(settings._module_name, 'tests.settings.xyz')

        # private __module_name object was loaded
        self.assertIsNotNone(settings._Settings__module_name)
        # os.env.get method must be called just one time
        m_os.environ.get.assert_called_once_with('SETTINGS', None)

    @mock.patch('quicksets.loader.os')
    def test_module_name_property_never_calls_env_get_method(self, m_os):
        m_os.environ.get.return_value = 'tests.settings.xyz'

        settings = Settings(module_name='tests.settings.abc')
        for _ in range(0, 2):
            # here we twice take an access to the lazy object
            self.assertEqual(settings._module_name, 'tests.settings.abc')

        # private __module_name object was loaded
        self.assertIsNotNone(settings._Settings__module_name)
        # os.env.get method must never be called
        m_os.environ.get.assert_not_called()

    @mock.patch('quicksets.loader.os')
    def test_env_error_raises(self, m_os):
        m_os.environ.get.return_value = None

        settings = Settings()
        with self.assertRaises(EnvironmentError) as err_ctx:
            # here we take an access to the lazy object that can't be loaded
            _ = settings._module_name
            self.assertEqual(
                err_ctx.exception.args[0],
                'ENV "SETTINGS" variable was not set. '
                'Please setup it like: '
                '`export SETTINGS="myapp.settings.production"` '
                'or simple use Settings class with module_name arg.'
            )

        # private __module_name object was not loaded
        self.assertIsNone(settings._Settings__module_name)
        # os.env.get method must be called just one time
        m_os.environ.get.assert_called_once_with('SETTINGS', None)

    def test_magic_methods_access_works_correctly(self):
        settings = Settings()

        self.assertEqual(settings.__class__, Settings)
        self.assertEqual([
            attr_name for attr_name in dir(settings)
            if not attr_name.startswith('__') and
               not attr_name.startswith('_Settings')
        ], [
            '_load',
            '_module_name',
            '_settings',
            'env_variable',
        ])

    @mock.patch('quicksets.loader.os')
    def test_env_variable_override(self, m_os):
        m_os.environ.get.return_value = 'tests.settings.xyz'

        class MySettings(Settings):
            env_variable = 'MY_SETTINGS'

        settings = MySettings()
        for _ in range(0, 2):
            # here we twice take an access to the lazy object
            self.assertEqual(settings._module_name, 'tests.settings.xyz')

        # it uses overridden env variable now
        m_os.environ.get.assert_called_once_with('MY_SETTINGS', None)

    def test_default_settings_dynamic_property(self):
        settings = Settings('tests.settings.default')

        self.assertDictEqual(settings.POSTGRESQL_CONNECTION_OPTIONS, {
            'user': 'postgres',
            'password': None,
            'host': 'localhost',
            'port': 5432,
            'database': 'postgres',
            'minsize': 4,
            'maxsize': 32,
            'pool_recycle': True,
        })

    def test_develop_settings_dynamic_property(self):
        settings = Settings('tests.settings.develop')

        self.assertDictEqual(settings.POSTGRESQL_CONNECTION_OPTIONS, {
            'user': 'postgres',
            'password': None,
            'host': 'localhost',
            'port': 5432,
            'database': 'db',
            'minsize': 4,
            'maxsize': 32,
            'pool_recycle': True,
        })

    def test_testing_settings_dynamic_property(self):
        settings = Settings('tests.settings.testing')

        self.assertDictEqual(settings.POSTGRESQL_CONNECTION_OPTIONS, {
            'user': 'postgres',
            'password': None,
            'host': 'localhost',
            'port': 5432,
            'database': 'db_test',
            'minsize': 4,
            'maxsize': 32,
            'pool_recycle': True,
        })

    def test_product_settings_dynamic_property(self):
        settings = Settings('tests.settings.product')

        self.assertDictEqual(settings.POSTGRESQL_CONNECTION_OPTIONS, {
            'user': 'prod_user',
            'password': '?????????',
            'host': '10.0.0.1',
            'port': 5432,
            'database': 'db_prod',
            'minsize': 4,
            'maxsize': 32,
            'pool_recycle': True,
        })


if __name__ == '__main__':
    unittest.main()
