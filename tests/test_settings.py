import unittest
import libs.qpanel.settings as qp_set
import os
from libs.qpanel import utils
import json


class UtilsTestClass(unittest.TestCase):

    def test_path_root(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        root = os.path.join(dirname, os.pardir)
        a = os.path.normpath(root)
        b = os.path.normpath(qp_set.ROOT_PATH)
        self.assertEqual(a, b)

    def test_data_setting(self):
        data_ok = json.loads(open(os.path.join(
            qp_set.ROOT_PATH, 'tests', 'data', 'setting.json')).read())

        data_error1 = json.loads(open(os.path.join(
            qp_set.ROOT_PATH, 'tests', 'data', 'setting_error1.json')).read())

        self.assertEqual(
            utils.validate_schema_data(data_ok, qp_set.schema_settings), True)

        self.assertIsNot(
            utils.validate_schema_data(
                data_error1, qp_set.schema_settings), True)


# runs the unit tests
if __name__ == '__main__':
    unittest.main()
