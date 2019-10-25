import unittest
from qpanel.convert import convert_time_when_param


class ConvertTestClass(unittest.TestCase):

    def test_convert_time_when_param(self):
        value = 'test1,00:00:00'
        self.assertEqual(convert_time_when_param(value),
                         {'when': 'test1', 'hour': '00:00:00'})

    def test_convert_time_without_hour(self):
        """ Should return a default hour in 00:00:00"""
        value = 'test1'
        self.assertEqual(convert_time_when_param(value),
                         {'when': 'test1', 'hour': '00:00:00'})

    def test_convert_time_first_second_hour(self):
        """ Should return a default hour in 00:00:01"""
        value = 'test1, 00:00:01'
        self.assertEqual(convert_time_when_param(value),
                         {'when': 'test1', 'hour': '00:00:01'})

    def test_convert_time_wrong_value_time(self):
        """ Should return a default hour"""
        value = 'test1, string_wrong'
        self.assertEqual(convert_time_when_param(value),
                         {'when': 'test1', 'hour': '00:00:00'})

    def test_convert_time_with_value_for_splitter(self):
        """Return value using other splitter"""
        value = 'test1; 00:00:01'
        self.assertEqual(convert_time_when_param(value, splitter=';'),
                         {'when': 'test1', 'hour': '00:00:01'})

    def test_convert_time_with_hour_in_large_format(self):
        """Return value for large hour"""
        value = 'test1; 15:51:01'
        self.assertEqual(convert_time_when_param(value, splitter=';'),
                         {'when': 'test1', 'hour': '15:51:01'})

    def test_convert_time_with_hour_short(self):
        """Return value for large hour"""
        value = 'test1; 5:51:01'
        self.assertEqual(convert_time_when_param(value, splitter=';'),
                         {'when': 'test1', 'hour': '05:51:01'})

    def test_convert_time_with_cero_hour(self):
        """Return value for large hour"""
        value = 'test1; 05:51:01'
        self.assertEqual(convert_time_when_param(value, splitter=';'),
                         {'when': 'test1', 'hour': '05:51:01'})


# runs the unit tests
if __name__ == '__main__':
    unittest.main()
