import unittest
from qpanel.utils import clean_str_to_div_id, underscore_to_camelcase, \
    timedelta_from_field_dict
from qpanel.convert import convert_time_when_param
import time
import datetime

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

    def test_timedelta_from_field_dict(self):
        now = time.time()
        d = {'time': now, 'time2': 'hola'}
        self.assertEqual(timedelta_from_field_dict('time', d, now + 1), datetime.timedelta(0, 1))
        self.assertNotEqual(timedelta_from_field_dict('time', d, now + 1), datetime.timedelta(0, 10))
        self.assertEqual(timedelta_from_field_dict('time', d, now + 100), datetime.timedelta(0, 100))
        self.assertEqual(timedelta_from_field_dict('timeno', d, now + 100), datetime.timedelta(0, 0))
        self.assertEqual(str(timedelta_from_field_dict('time', d, now + 1)), '0:00:01')
        self.assertEqual(timedelta_from_field_dict('time', d, now), datetime.timedelta(0, 0))
        self.assertEqual(str(timedelta_from_field_dict('time', d, now)), '0:00:00')

        d2 = {'time': 60, 'time2': 6001}
        self.assertEqual(str(timedelta_from_field_dict('time', d2, None, True)), '0:01:00')
        self.assertEqual(str(timedelta_from_field_dict('time2', d2, None, True)), '1:40:01')

    def test_convert_time_when_param(self):
        value = 'test1,00:00:00'
        self.assertEqual(convert_time_when_param(value),
                         {'when': 'test1', 'hour': '00:00:00'})

        value = 'test1'
        self.assertEqual(convert_time_when_param(value),
                         {'when': 'test1', 'hour': '00:00:00'})

        value = 'test1, 00:00:01'
        self.assertEqual(convert_time_when_param(value),
                         {'when': 'test1', 'hour': '00:00:01'})

        value = 'test1, string_wrong'
        self.assertEqual(convert_time_when_param(value),
                         {'when': 'test1', 'hour': '00:00:00'})

        value = 'test1; 00:00:01'
        self.assertEqual(convert_time_when_param(value, splitter=';'),
                         {'when': 'test1', 'hour': '00:00:01'})



# runs the unit tests
if __name__ == '__main__':
    unittest.main()
