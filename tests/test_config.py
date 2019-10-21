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

    """
        user_queues
        tests/data/configs/user_queue/
            no-section.ini
            section-with-config.ini
            section-without-config.ini
    """

    def test_user_queues_without_section(self):
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'user_queues', 'no-section.ini')
        configuration = config.QPanelConfig()
        self.assertFalse(configuration.has_user_queues())
        self.assertEqual(
            configuration.queue_enables_for_username('nobody'), [])
        self.assertTrue(
            configuration.enable_queue_for_user(
                'nobody', 'testing'))

    def test_user_queues_section_without_config(self):
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'user_queues', 'section-without-config.ini')
        configuration = config.QPanelConfig()
        self.assertFalse(configuration.has_user_queues())
        self.assertEqual(
            configuration.queue_enables_for_username('nobody'), [])
        self.assertTrue(
            configuration.enable_queue_for_user(
                'nobody', 'testing'))

    def test_user_queues_with_config(self):
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'user_queues', 'section-with-config.ini')
        configuration = config.QPanelConfig()
        self.assertTrue(configuration.has_user_queues())
        self.assertEqual(len(configuration.get_items('user_queues')), 2)
        self.assertEqual(
            configuration.queue_enables_for_username('rodrigo'), [
                'support', 'commercial'])
        self.assertEqual(
            configuration.queue_enables_for_username('ramirez'),
            ['agents'])
        self.assertEqual(
            configuration.queue_enables_for_username('nobody'), [])
        self.assertTrue(
            configuration.enable_queue_for_user(
                'rodrigo', 'support'))
        self.assertFalse(
            configuration.enable_queue_for_user(
                'nobody', 'testing'))

    def test_realname_queue(self):
        """ Should return the same name if not rename"""
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'config_default.ini')

        configuration = config.QPanelConfig()
        self.assertEqual(configuration.realname_queue("s_cl"), "s_cl")

    def test_realname_queue_with_rename(self):
        """ Should return the same name if not rename"""
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'config_rename_queue.conf')

        configuration = config.QPanelConfig()
        self.assertEqual(configuration.realname_queue("s_cl"), "s_cl")
        self.assertEqual(configuration.realname_queue("support"), "5000")


# runs the unit tests
if __name__ == '__main__':
    unittest.main()
