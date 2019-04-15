import os
import unittest
from shutil import copyfile


class ConfigTestClass(unittest.TestCase):

    def setUp(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        self.configs_dir = os.path.join(dirname, 'data', 'configs')
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'config_default.ini')

        from  qpanel import app as qpanel_app
        qpanel_app.app.testing = True
        self.app = qpanel_app.app.test_client()

    def tearDown(self):
        if 'QPANEL_CONFIG_FILE' in os.environ:
            del os.environ["QPANEL_CONFIG_FILE"]

    def test_default_run(self):
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'config_default.ini')

        rs = self.app.get('/')
        self.assertEqual(rs.status_code, 200)
        self.assertIn('REQUEST_INTERVAL = 5000', str(rs.data))

