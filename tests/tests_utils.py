import unittest
from libs.qpanel.utils import clean_str_to_div_id


class UtilsTestClass(unittest.TestCase):

    def test_clean_str_to_div(self):
        div = 'ro/.d. i _@l_k/d_@'
        self.assertEqual(clean_str_to_div_id(div),  'ro-_d_ i __l_k-d__')

# runs the unit tests
if __name__ == '__main__':
    unittest.main()
