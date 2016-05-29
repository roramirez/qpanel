import unittest
from libs.qpanel.utils import clean_str_to_div_id, underscore_to_camelcase


class UtilsTestClass(unittest.TestCase):

    def test_clean_str_to_div(self):
        div = 'ro/.d. i _@l_k/d_@'
        self.assertEqual(clean_str_to_div_id(div),  'ro-_d_ i __l_k-d__')

    def test_underscore_to_camelcase(self):
        a = 'rodrigoRamirez'
        self.assertEquals(underscore_to_camelcase(a), 'Rodrigoramirez')
        a = 'rodrigo_Ramirez'
        self.assertEqual(underscore_to_camelcase(a), 'RodrigoRamirez')
        a = 'rodrigo_ramirez'
        self.assertEqual(underscore_to_camelcase(a), 'RodrigoRamirez')
        a = '_rodrigo_ramirez'
        self.assertEqual(underscore_to_camelcase(a), '_RodrigoRamirez')

# runs the unit tests
if __name__ == '__main__':
    unittest.main()
