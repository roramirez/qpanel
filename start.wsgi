import sys
import os
dirname, filename = os.path.split(os.path.abspath(__file__))

sys.path.insert(0, dirname)
def application(req_environ, start_response):
    if "QPANEL_CONFIG_FILE" in req_environ:
        os.environ['QPANEL_CONFIG_FILE'] = req_environ['QPANEL_CONFIG_FILE']
    from qpanel.app import app as _application
    return _application(req_environ, start_response)
