import os
import json

dirname, filename = os.path.split(os.path.abspath(__file__))
ROOT_PATH = os.path.join(dirname, os.pardir, os.pardir)
PATH_FILE_CONFIG = os.path.join(ROOT_PATH, 'config.ini')

schema_settings = json.loads(
    open(os.path.join(ROOT_PATH, 'data', 'settings.schema.json')).read())
