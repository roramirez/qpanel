import os
import unittest

import mock
import pytest

from qpanel import backend


class TestBackend:
    def setup_method(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        self.configs_dir = os.path.join(dirname, "data", "configs")

    @pytest.mark.parametrize(
        "lang,expected", [("es", "6 minutos"), ("en", "6 minutes")]
    )
    @mock.patch("flask_babel.get_locale")
    @mock.patch("qpanel.asterisk.AsteriskAMI.connect_ami")
    def test_eval(self, mock, mock_locale, lang, expected):
        mock_locale.return_value = lang
        os.environ["QPANEL_CONFIG_FILE"] = os.path.join(
            self.configs_dir, "config_default.ini"
        )

        test_backend = backend.Backend()
        data = {
            "commercial": {
                "Max": "0",
                "Strategy": "ringall",
                "Calls": "1",
                "Holdtime": "0",
                "TalkTime": "0",
                "Completed": "0",
                "Abandoned": "0",
                "ServiceLevel": "0",
                "ServicelevelPerf": "0.0",
                "Weight": "0",
                "members": {
                    "SIP/1236": {
                        "Name": "SIP/1236",
                        "StateInterface": "SIP/1236",
                        "Membership": "dynamic",
                        "Penalty": "0",
                        "CallsTaken": "0",
                        "LastCall": "0",
                        "IsInCall": "0",
                        "Status": "4",
                        "Paused": "0",
                    }
                },
                "entries": {
                    "channel_1": {
                        "Position": "1",
                        "Channel": "<Asterisk.Manager.BaseChannel referencing channel 'Console/dsp' of <Asterisk.Manager.Manager connected as rodrigo to localhost:5038>>",
                        "Uniqueid": "1654441088.0",
                        "CallerIDNum": "unknown",
                        "CallerIDName": "unknown",
                        "ConnectedLineNum": "unknown",
                        "ConnectedLineName": "unknown",
                        "Wait": "368",
                    }
                },
            },
            "pagos_saldos": {
                "Max": "0",
                "Strategy": "rrmemory",
                "Calls": "0",
                "Holdtime": "0",
                "TalkTime": "0",
                "Completed": "0",
                "Abandoned": "0",
                "ServiceLevel": "0",
                "ServicelevelPerf": "0.0",
                "Weight": "0",
                "members": {
                    "Local/109@CallAgent": {
                        "Name": "PJSIP/109",
                        "StateInterface": "PJSIP/109",
                        "Membership": "static",
                        "Penalty": "0",
                        "CallsTaken": "0",
                        "LastCall": "0",
                        "IsInCall": "0",
                        "Status": "4",
                        "Paused": "0",
                    },
                    "Local/108@CallAgent": {
                        "Name": "PJSIP/108",
                        "StateInterface": "PJSIP/108",
                        "Membership": "static",
                        "Penalty": "0",
                        "CallsTaken": "0",
                        "LastCall": "0",
                        "IsInCall": "0",
                        "Status": "4",
                        "Paused": "0",
                    },
                    "Local/153@CallAgent": {
                        "Name": "PJSIP/153",
                        "StateInterface": "PJSIP/153",
                        "Membership": "static",
                        "Penalty": "0",
                        "CallsTaken": "0",
                        "LastCall": "0",
                        "IsInCall": "0",
                        "Status": "4",
                        "Paused": "0",
                    },
                },
                "entries": {},
            },
            "proveedores": {
                "Max": "0",
                "Strategy": "rrmemory",
                "Calls": "0",
                "Holdtime": "0",
                "TalkTime": "0",
                "Completed": "0",
                "Abandoned": "0",
                "ServiceLevel": "0",
                "ServicelevelPerf": "0.0",
                "Weight": "0",
                "members": {
                    "Local/131@CallAgent": {
                        "Name": "PJSIP/131",
                        "StateInterface": "PJSIP/131",
                        "Membership": "static",
                        "Penalty": "0",
                        "CallsTaken": "0",
                        "LastCall": "0",
                        "IsInCall": "0",
                        "Status": "4",
                        "Paused": "0",
                    },
                    "Local/130@CallAgent": {
                        "Name": "PJSIP/130",
                        "StateInterface": "PJSIP/130",
                        "Membership": "static",
                        "Penalty": "0",
                        "CallsTaken": "0",
                        "LastCall": "0",
                        "IsInCall": "0",
                        "Status": "4",
                        "Paused": "0",
                    },
                },
                "entries": {},
            },
        }

        result = test_backend.parse_asterisk(data=data)
        assert result["commercial"]["entries"]["channel_1"]["WaitAgo"] == expected
