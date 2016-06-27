import unittest
import libs.qpanel.settings as qp_set
import os


class UtilsTestClass(unittest.TestCase):

    def test_path_root(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        root = os.path.join(dirname, os.pardir)
        a = os.path.normpath(root)
        b = os.path.normpath(qp_set.ROOT_PATH)
        self.assertEqual(a, b)


# runs the unit tests
if __name__ == '__main__':
    unittest.main()
