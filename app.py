from flask import Flask, render_template, jsonify
import os, sys
import ConfigParser
import json
from distutils.util import strtobool

# get current names for directory and file
dirname, filename = os.path.split(os.path.abspath(__file__))

# py-asterisk
sys.path.append(os.path.join(dirname,  'libs','py-asterisk'))
from Asterisk.Manager import *


app = Flask(__name__)

# config file
cfg_file = 'config.ini'
cfg = ConfigParser.ConfigParser()
cfg.read(os.path.join(dirname, cfg_file))

def __connect_manager():
    host = cfg.get('manager', 'host')
    port = int(cfg.get('manager', 'port'))
    user = cfg.get('manager', 'user')
    password = cfg.get('manager', 'password')
    try:
        manager = Manager((host, port), user, password)
        return manager
    except:
        app.logger.info('Error to connect to Asterisk Manager. Check config.ini and manager.conf of asterisk')
manager = __connect_manager()

def is_debug():
    try:
        var = cfg.get('general', 'debug')
        v = True if strtobool(var) == 1 else False
    except:
        return False
    return v

def port_bind():
    try:
        var = cfg.get('general', 'port')
        v = int(var)
    except:
        return 5000
    return v

def __get_data_queues_manager():
    try:
        data = manager.QueueStatus()
    except:
        app.logger.info('Error to connect to Asterisk Manager. Check config.ini and manager.conf of asterisk')
        data = []
    return data


def get_data_queues(queue = None):
    data = parser_data_queue(__get_data_queues_manager())
    if queue is not None:
        data = data[queue]
    if is_debug():
        app.logger.debug(data)
    return data


def parser_data_queue(data):
    # convert references manager to string
    for q in data:
        for e in data[q]['entries']:
            tmp = data[q]['entries'].pop(e)
            data[q]['entries'][str(e)] = tmp
            tmp = data[q]['entries'][str(e)]['Channel']
            data[q]['entries'][str(e)]['Channel']  = str(tmp)
        for m in data[q]['members']:
            #Asterisk 1.8 dont have StateInterface
            if 'StateInterface' not in data[q]['members'][m]:
                data[q]['members'][m]['StateInterface'] = m
    return data


@app.before_first_request
def setup_logging():
  # issue https://github.com/benoitc/gunicorn/issues/379
  if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


#Utilities helpers
@app.context_processor
def utility_processor():
    def format_id_agent(value):
        return value.replace('/', '-')
    return dict(format_id_agent=format_id_agent)

@app.context_processor
def utility_processor():
    def str_status_agent(value):
        try:
            value = int(value)
        except:
            value = 0
        unavailable = [0, 2, 5]
        free = [1]

        if value in unavailable:
            return 'unavailable'
        elif value in free:
            return 'free'
        else:
            return 'busy'
    return dict(str_status_agent=str_status_agent)

# ---------------------
# ---- Routes ---------
# ---------------------
# home
@app.route('/')
def home():
    data = get_data_queues()
    return render_template('index.html', queues = data)


@app.route('/queue/<name>')
def queue(name = None):
    data = get_data_queues(name)
    return render_template('queue.html', data = data, name = name)


@app.route('/queue/<name>.json')
def queue_json(name = None):
    data = get_data_queues(name)
    return jsonify(
        name = name,
        data = data
    )

# data queue
@app.route('/queues')
def queues():
    data = get_data_queues()
    return jsonify(
        data = data
    )

# ---------------------
# ---- Main  ----------
# ---------------------
if __name__ == '__main__':
    if is_debug():
        app.debug = True
    app.run(host='0.0.0.0', port=port_bind())
