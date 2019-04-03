import os
import unittest
from qpanel import config
from shutil import copyfile


class ConfigTestClass(unittest.TestCase):

    def setUp(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        self.configs_dir = os.path.join(dirname, 'data', 'configs')
        self.default_file_config = os.path.join(
            self.configs_dir, os.pardir, os.pardir,
            os.pardir, 'config.ini')

    def tearDown(self):
        if 'QPANEL_CONFIG_FILE' in os.environ:
            del os.environ["QPANEL_CONFIG_FILE"]

    def test_configuration_file_enviroment_variable(self):
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'config_default.ini')
        configuration = config.QPanelConfig()
        self.assertEqual(configuration.port_bind, 5010)

    def test_configuration_file_enviroment_variable_not_found(self):
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'config_no_found')
        with self.assertRaises(config.NotConfigFileQPanel):
            config.QPanelConfig()

    def test_configuration_without_fileconfig(self):
        if ('CI' in os.environ or
                os.path.isfile(self.default_file_config) is False):
            with self.assertRaises(config.NotConfigFileQPanel):
                config.QPanelConfig()

    def test_sample_file_configuration(self):
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, os.pardir, os.pardir,
            os.pardir, 'samples', 'config.ini-dist')

        configuration = config.QPanelConfig()
        self.assertEqual(configuration.port_bind, 5000)

    def test_has_section(self):
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'config_default.ini')
        configuration = config.QPanelConfig()
        self.assertEqual(configuration.has_section('general'), True)

    def test_has_no_section(self):
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'config_default.ini')
        configuration = config.QPanelConfig()
        self.assertEqual(configuration.has_section('general_not_found'), False)

    def test_default_theme_config(self):
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'config_default.ini')
        configuration = config.QPanelConfig()
        self.assertEqual(configuration.theme, 'qpanel')

    def test_old_theme_config(self):
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'config_old_theme.ini')
        configuration = config.QPanelConfig()
        self.assertEqual(configuration.theme, 'old')

    def test_wrong_theme_config(self):
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'config_wrong_theme.ini')
        configuration = config.QPanelConfig()
        self.assertEqual(configuration.theme, 'qpanel')

    def test_use_config_ini_default(self):
        """
            This test only run if the config.ini in the root path
            is not present.
            This create a new file in this directory and test the
            configuration file.
        """
        if os.path.isfile(self.default_file_config) is False:
            file_sample = os.path.join(self.configs_dir, 'config_default.ini')
            copyfile(file_sample, self.default_file_config)
            configuration = config.QPanelConfig()
            os.remove(self.default_file_config)
            self.assertEqual(configuration.port_bind, 5010)


# runs the unit tests
if __name__ == '__main__':
    unittest.main()
