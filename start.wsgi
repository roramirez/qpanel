import sys
import os
dirname, filename = os.path.split(os.path.abspath(__file__))

sys.path.insert(0, dirname)
from qpanel.app import app as application
