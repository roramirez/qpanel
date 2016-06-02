import unittest
from libs.qpanel.upgrader import __first_line as firstline

class UpgradeTestClass(unittest.TestCase):

    def test_first_line(self):
        content = 'a\n\b\t\b'
        self.assertEqual(firstline(content),  'a')
        self.assertNotEqual(firstline(content),  'ab')


# runs the unit tests
if __name__ == '__main__':
    unittest.main()
