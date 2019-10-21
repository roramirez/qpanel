import os
import unittest
from qpanel import asterisk
import mock
from unittest.mock import call


class AsteriskTestClass(unittest.TestCase):

    def setUp(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        self.configs_dir = os.path.join(dirname, 'data', 'configs')

    @mock.patch('qpanel.asterisk.AsteriskAMI.connect_ami')
    def test_spy_async_keyword(self, mock):
        """
            Should not failed with by async rename keyword introduced
            in Python 3.8
        """
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, 'config_default.ini')

        ami = asterisk.AsteriskAMI('host', 5438, 'user', 'password')
        ami.spy('test/channel', 'SIP/a')
        assert mock.mock_calls == [call(),
                                   call().Originate('SIP/a',
                                                    application='ChanSpy',
                                                    async_param='yes',
                                                    data='test/channel,q')]
