import os

dirname, filename = os.path.split(os.path.abspath(__file__))
PATH_FILE_CONFIG = os.path.join(dirname, os.pardir,
                                os.pardir, 'config.ini')
