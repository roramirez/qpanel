import sys
import os
dirname, filename = os.path.split(os.path.abspath(__file__))

sys.path.insert(0, dirname)
from app import app as application
