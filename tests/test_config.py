import os
import unittest
from qpanel import config


class ConfigTestClass(unittest.TestCase):

    def setUp(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        self.configs_dir = os.path.join(dirname, 'data', 'configs')

    def tearDown(self):
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

# runs the unit tests
if __name__ == '__main__':
    unittest.main()
