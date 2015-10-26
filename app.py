from flask import Flask, render_template, jsonify, redirect, request, session, url_for
import os, sys
import ConfigParser
import json
from distutils.util import strtobool
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.exceptions import abort

# babel
from flask.ext.babel import Babel, gettext

# get current names for directory and file
dirname, filename = os.path.split(os.path.abspath(__file__))

# py-asterisk
sys.path.append(os.path.join(dirname,  'libs','py-asterisk'))
from Asterisk.Manager import *

# config file
cfg_file = 'config.ini'
cfg = ConfigParser.ConfigParser()
try:
    with open(os.path.join(dirname, cfg_file))  as f:
        cfg.readfp(f)
except IOError:
    print 'Error open file config. Check if config.ini exists'
    sys.exit()


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

def is_debug():
    try:
        var = cfg.get('general', 'debug')
        v = True if strtobool(var) == 1 else False
    except:
        return False
    return v

def port_bind():
    return int(__get_entry_ini_default('general', 'port', 5000))

def host_bind():
    return __get_entry_ini_default('general', 'host', '0.0.0.0')

def get_hide_config():
    tmp = __get_entry_ini_default('general', 'hide', '')
    tmp = tmp.replace('\'', '')
    return tmp.split(',')


def __get_entry_ini_default(section, var, default):
    try:
        var = cfg.get(section, var)
        v = var
    except:
        return default
    return v

def __get_data_queues_manager():
    manager = __connect_manager()
    try:
        data = manager.QueueStatus()
    except:
        app.logger.info('Error to connect to Asterisk Manager. Check config.ini and manager.conf of asterisk')
        data = []
    return data


def get_data_queues(queue = None):
    data = parser_data_queue(__get_data_queues_manager())
    if queue is not None:
        try:
            data = data[queue]
        except:
            abort(404)
    if is_debug():
        app.logger.debug(data)
    return data

def hide_queue(data):
    tmp_data = {}
    hide = get_hide_config()
    for q in data:
        if q not in hide:
            tmp_data[q] = data[q]
    return tmp_data

def rename_queue(data):
    tmp_data = {}
    for q in data:
        rename = __get_entry_ini_default('rename', q, None)
        if rename is not None:
            tmp_data[rename] = data[q]
        else:
            tmp_data[q] = data[q]
    return tmp_data



def parser_data_queue(data):
    data = hide_queue(data)
    data = rename_queue(data)
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


# Flask env
APPLICATION_ROOT = __get_entry_ini_default('general', 'base_url', '/')
app = Flask(__name__)
app.config.from_object(__name__)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = __get_entry_ini_default('general', 'language', 'en')

@app.before_first_request
def setup_logging():
    # issue https://github.com/benoitc/gunicorn/issues/379
    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)

# babel
@babel.localeselector
def get_locale():
    browser = request.accept_languages.best_match(['en', 'es', 'de'])
    try:
      app.logger.debug(session['language'])
      return session['language']
    except KeyError:
      session['language'] = browser
      app.logger.debug(session['language'])
      return browser

#Utilities helpers
@app.context_processor
def utility_processor():
    def format_id_agent(value):
        v = value.replace('/', '-')
        return v.replace('@', '_')
    return dict(format_id_agent=format_id_agent)

@app.context_processor
def utility_processor():
    def str_status_agent(value):
        try:
            value = int(value)
        except:
            value = 0
        unavailable = [0, 4, 5]
        free = [1]

        if value in unavailable:
            return gettext('unavailable')
        elif value in free:
            return gettext('free')
        else:
            return gettext('busy')
    return dict(str_status_agent=str_status_agent)

@app.context_processor
def utility_processor():
    def request_interval():
        return int(__get_entry_ini_default('general', 'interval', 5)) * 1000
    return dict(request_interval=request_interval)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



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

@app.route('/lang')
def fake_language():
    return redirect(url_for('home'))
@app.route('/lang/<language>')
def language(language = None):
    session['language'] = language
    return redirect(url_for('home'))

# ---------------------
# ---- Main  ----------
# ---------------------
if __name__ == '__main__':

    if is_debug():
        app.config['DEBUG'] = True

    app.secret_key = __get_entry_ini_default('general', 'secret_key', 'CHANGEME_ON_CONFIG')

    app.logger.debug(APPLICATION_ROOT)
    if APPLICATION_ROOT == '/':
        app.run(host=host_bind(), port=port_bind())
    else:
        application = DispatcherMiddleware(Flask('dummy_app'), {
            app.config['APPLICATION_ROOT']: app,
        })
        run_simple(host_bind(), port_bind(), application, use_reloader=True)
