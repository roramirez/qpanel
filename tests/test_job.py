import os
import unittest
from qpanel import job


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


# runs the unit tests
if __name__ == '__main__':
    unittest.main()
