# coding=utf8

# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#


from flask import Flask, render_template, jsonify, redirect, request, session, url_for
import os, sys
import ConfigParser
import json
from distutils.util import strtobool
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.exceptions import abort

# babel
from flask.ext.babel import Babel, gettext, dates, format_timedelta
from datetime import timedelta
# get current names for directory and file
dirname, filename = os.path.split(os.path.abspath(__file__))

#flask-login
import flask.ext.login as flask_login

# py-asterisk
sys.path.append(os.path.join(dirname,  'libs','py-asterisk'))
from Asterisk.Manager import *
from libs.qpanel.upgrader import *
from libs.qpanel.utils import *



class User(flask_login.UserMixin):
    pass

# config file
cfg_file = os.path.join(dirname, 'config.ini')
cfg = ConfigParser.ConfigParser()
try:
    with open(cfg_file)  as f:
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
    return __get_bool_value_config('general', 'debug', False)

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

def __get_bool_value_config(section, option, default):
    try:
        var = cfg.get(section, option)
        v = True if strtobool(var) == 1 else False
    except:
        return default
    return v

def __get_entry_int_min_value(section, option, min = 0):
    v = int(__get_entry_ini_default(section, option, min))
    if v < min:
        return min
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
    current_timestamp = int(time.time())
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

            second_ago = 0
            if 'LastCall' in data[q]['members'][m]:
                if int(data[q]['members'][m]['LastCall']) > 0:
                    second_ago = current_timestamp - int(data[q]['members'][m]['LastCall'])
            data[q]['members'][m]['LastCallAgo'] = format_timedelta(timedelta(seconds=second_ago), granularity='second')

            # Time last pause
            second_ago = 0
            if 'LastPause' in data[q]['members'][m]:
                if int(data[q]['members'][m]['LastPause']) > 0:
                    second_ago = current_timestamp - int(data[q]['members'][m]['LastPause'])
            data[q]['members'][m]['LastPauseAgo'] = format_timedelta(timedelta(seconds=second_ago), granularity='second')


        #REFACTORME
        for c in data[q]['entries']:
            second_ago = 0
            if 'Wait' in data[q]['entries'][c]:
                if int(data[q]['entries'][c]['Wait']) > 0:
                    second_ago = int(data[q]['entries'][c]['Wait'])
            data[q]['entries'][c]['WaitAgo'] = format_timedelta(timedelta(seconds=second_ago), granularity='second')



    return data


def get_user_config_by_name(username):
    try:
        user = User()
        user.id = username
        user.password = cfg.get('users', username)
        return user
    except:
        return None


# Flask env
APPLICATION_ROOT = __get_entry_ini_default('general', 'base_url', '/')
app = Flask(__name__)
app.config.from_object(__name__)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = __get_entry_ini_default('general', 'language', 'en')
app.secret_key = __get_entry_ini_default('general', 'secret_key', 'CHANGEME_ON_CONFIG')

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


def set_data_user(user_config):
    user = User()
    user.id = user_config.id
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

@login_manager.user_loader
def user_loader(username):
    user_config = get_user_config_by_name(username)
    if user_config is None:
        return
    return set_data_user(user_config)

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user_config = get_user_config_by_name(username)

    if count_element_sections_config('users', cfg) == 0:
        # fake login
        user = User()
        user.id = 'withoutlogin'
        return user

    if user_config is None:
        return

    user = set_data_user(user_config)
    user.is_authenticated = user_config == request.form['pw']
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if count_element_sections_config('users', cfg) == 0:
        return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    user_config = get_user_config_by_name(username)
    if user_config is None:
        return redirect(url_for('login'))

    if user_config.password == request.form['pw']:
        user = set_data_user(user_config)
        flask_login.login_user(user)
        return redirect(url_for('home'))
    return redirect(url_for('login'))




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
      return session['language']
    except KeyError:
      session['language'] = browser
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
        return (__get_entry_int_min_value('general', 'interval', 1) * 1000)
    return dict(request_interval=request_interval)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.context_processor
def utility_processor():
    def check_upgrade():
        return __get_bool_value_config('general', 'check_upgrade', True)
    return dict(check_upgrade=check_upgrade)

@app.context_processor
def utility_processor():
    def show_service_level():
        return __get_bool_value_config('general', 'show_service_level', False)
    return dict(show_service_level=show_service_level)

@app.context_processor
def utility_processor():
    def has_users():
        if count_element_sections_config('users', cfg) == 0:
            return False
        else:
            return True
    return dict(has_users=has_users)
# ---------------------
# ---- Routes ---------
# ---------------------
# home
@app.route('/')
@flask_login.login_required
def home():
    data = get_data_queues()
    return render_template('index.html', queues = data)



@app.route('/queue/<name>')
@flask_login.login_required
def queue(name = None):
    data = get_data_queues(name)
    return render_template('queue.html', data = data, name = name)


@app.route('/queue/<name>.json')
@flask_login.login_required
def queue_json(name = None):
    data = get_data_queues(name)
    return jsonify(
        name = name,
        data = data
    )



# data queue
@app.route('/queues')
@flask_login.login_required
def queues():
    data = get_data_queues()
    return jsonify(
        data = data
    )



@app.route('/lang')
@flask_login.login_required
def fake_language():
    return redirect(url_for('home'))
@app.route('/lang/<language>')
@flask_login.login_required
def language(language = None):
    session['language'] = language
    return redirect(url_for('home'))


@app.route('/check_new_version')
@flask_login.login_required
def check_new_version():
    need_upgrade = False
    try:
        if require_upgrade():
            need_upgrade = True
    except:
        pass

    return jsonify(
        require_upgrade = need_upgrade,
        current_version = get_current_version(),
        last_stable_version = get_stable_version()
    )

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

# ---------------------
# ---- Main  ----------
# ---------------------
if __name__ == '__main__':

    if is_debug():
        app.config['DEBUG'] = True


    if APPLICATION_ROOT == '/':
        app.run(host=host_bind(), port=port_bind(), extra_files=[cfg_file])
    else:
        application = DispatcherMiddleware(Flask('dummy_app'), {
            app.config['APPLICATION_ROOT']: app,
        })
        run_simple(host_bind(), port_bind(), application, use_reloader=True, extra_files=[cfg_file])
