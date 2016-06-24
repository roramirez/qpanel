import shutil
import tempfile
from os import path
import unittest
from libs.qpanel.upgrader import __first_line as firstline, get_current_version


class UpgradeTestClass(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_first_line(self):
        content = 'a\n\b\t\b'
        self.assertEqual(firstline(content),  'a')
        self.assertNotEqual(firstline(content),  'ab')

    def test_version(self):
        version = '0.10'
        version_file = path.join(self.test_dir, 'VERSION')
        f = open(version_file, 'w')
        f.write(version)
        f.close()
        self.assertEqual(get_current_version(version_file), version)
        self.assertNotEqual(get_current_version(version_file), '0.11.0')


# runs the unit tests
if __name__ == '__main__':
    unittest.main()
