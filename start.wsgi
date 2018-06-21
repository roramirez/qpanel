import sys
import os
dirname, filename = os.path.split(os.path.abspath(__file__))

sys.path.insert(0, dirname)
def application(req_environ, start_response):
    if req_environ.has_key("QPANEL_CONFIG_FILE"):
        os.environ['QPANEL_CONFIG_FILE'] = req_environ['QPANEL_CONFIG_FILE']
    from qpanel.app import app as _application
    return _application(req_environ, start_response)
