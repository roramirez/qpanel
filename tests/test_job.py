import os
import unittest
from qpanel import job
import mock
from datetime import datetime


class JobTestClass(unittest.TestCase):

    def setUp(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        self.configs_dir = os.path.join(dirname, 'data', 'configs')
        self.default_file_config = os.path.join(
            self.configs_dir, os.pardir, os.pardir,
            os.pardir, 'config.ini')

    def tearDown(self):
        if 'QPANEL_CONFIG_FILE' in os.environ:
            del os.environ["QPANEL_CONFIG_FILE"]

    def test_exists_job_onconfig_variable(self):
        """ Should return True or False if entry exists
           in configuration file

            [reset_stats]
            support = daily,00:00:00
            commercial= daily,00:10:00

        """
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'resetstats/two.ini')

        self.assertFalse(
            job.exists_job_onconfig(
                'support',
                'daily',
                '00:00:10'))
        self.assertFalse(
            job.exists_job_onconfig(
                'support',
                'weekly',
                '00:00:00'))
        self.assertTrue(
            job.exists_job_onconfig(
                'support',
                'daily',
                '00:00:00'))
        self.assertTrue(
            job.exists_job_onconfig(
                'commercial',
                'daily',
                '00:10:00'))

    def test_get_days_from_val(self):
        self.assertEqual(job.get_days_from_val('daily'), 1)
        self.assertEqual(job.get_days_from_val('Daily'), 1)
        self.assertEqual(job.get_days_from_val('weekly'), 7)
        self.assertEqual(job.get_days_from_val('monthly'), 30)
        self.assertEqual(job.get_days_from_val('mon'), 7)
        self.assertEqual(job.get_days_from_val('p'), 0)

    def test_give_day_number(self):
        """Should return a correct day number for key configuration"""
        self.assertEqual(job.give_day_number('mon'), 0)
        self.assertEqual(job.give_day_number('tue'), 1)
        self.assertEqual(job.give_day_number('wed'), 2)
        self.assertEqual(job.give_day_number('thu'), 3)
        self.assertEqual(job.give_day_number('fri'), 4)
        self.assertEqual(job.give_day_number('sat'), 5)
        self.assertEqual(job.give_day_number('sun'), 6)

        self.assertEqual(job.give_day_number('weekly'), 0)  # First day of week


class DateTimeFromConfigTestClass(unittest.TestCase):

    @mock.patch('qpanel.job.get_now')
    def test_daily_today(self, mock):
        """ Should return at the same day"""
        mock.return_value = datetime(2019, 11, 1, 20, 50, 30)
        self.assertEqual(job.datetime_from_config('daily', '23:50:50'),
                         datetime(2019, 11, 1, 23, 50, 50)
                         )

    @mock.patch('qpanel.job.get_now')
    def test_daily_tomorrow(self, mock):
        """ Should return at the next day"""
        mock.return_value = datetime(2019, 11, 1, 20, 50, 30)
        self.assertEqual(job.datetime_from_config('daily', '19:50:50'),
                         datetime(2019, 11, 2, 19, 50, 50)
                         )

    @mock.patch('qpanel.job.get_now')
    def test_monthy_next_month(self, mock):
        """ Should return at the next month"""
        mock.return_value = datetime(2019, 11, 1, 20, 50, 30)
        self.assertEqual(job.datetime_from_config('monthly', '19:50:50'),
                         datetime(2019, 12, 1, 19, 50, 50)
                         )

    @mock.patch('qpanel.job.get_now')
    def test_monthy_today(self, mock):
        """ Should return at the next month"""
        mock.return_value = datetime(2019, 11, 1, 20, 50, 30)
        self.assertEqual(job.datetime_from_config('monthly', '22:50:50'),
                         datetime(2019, 11, 1, 22, 50, 50)
                         )

    @mock.patch('qpanel.job.get_now')
    def test_fri_today(self, mock):
        """ Should return at the today """
        mock.return_value = datetime(2019, 11, 1, 20, 50, 30)
        self.assertEqual(job.datetime_from_config('fri', '22:50:50'),
                         datetime(2019, 11, 1, 22, 50, 50)
                         )

    @mock.patch('qpanel.job.get_now')
    def test_next_friday(self, mock):
        """ Should return the next friday today """
        mock.return_value = datetime(2019, 11, 1, 20, 50, 30)
        self.assertEqual(job.datetime_from_config('fri', '19:50:50'),
                         datetime(2019, 11, 8, 19, 50, 50)
                         )

    @mock.patch('qpanel.job.get_now')
    def test_next_monday(self, mock):
        """ Should return the next friday today """
        mock.return_value = datetime(2019, 11, 1, 20, 50, 30)
        self.assertEqual(job.datetime_from_config('mon', '19:50:50'),
                         datetime(2019, 11, 4, 19, 50, 50)
                         )

    @mock.patch('qpanel.job.get_now')
    def test_weekly_next_monday(self, mock):
        """ Should return the next friday today """
        mock.return_value = datetime(2019, 11, 1, 20, 50, 30)
        self.assertEqual(job.datetime_from_config('weekly', '19:50:50'),
                         datetime(2019, 11, 4, 19, 50, 50)
                         )

    @mock.patch('qpanel.job.get_now')
    def test_weekly_today(self, mock):
        """ Should return the next friday today """
        mock.return_value = datetime(2019, 11, 4, 15, 50, 30)
        self.assertEqual(job.datetime_from_config('weekly', '19:50:50'),
                         datetime(2019, 11, 4, 19, 50, 50)
                         )

    @mock.patch('qpanel.job.get_now')
    def test_weekly_next_week_monday(self, mock):
        """ Should return the next friday today """
        mock.return_value = datetime(2019, 11, 4, 15, 50, 30)
        self.assertEqual(job.datetime_from_config('weekly', '10:50:50'),
                         datetime(2019, 11, 11, 10, 50, 50)
                         )


# runs the unit tests
if __name__ == '__main__':
    unittest.main()
