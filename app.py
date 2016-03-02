# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#


from flask import Flask, render_template, jsonify, redirect,\
    request, session, url_for
import os
import sys
import ConfigParser
import json
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.exceptions import abort

# babel
from flask.ext.babel import Babel, gettext, dates, format_timedelta
from datetime import timedelta

# flask-login
import flask.ext.login as flask_login

from libs.qpanel.upgrader import *
import libs.qpanel.utils as uqpanel

from libs.qpanel.config import QPanelConfig
from libs.qpanel.backend import Backend


class User(flask_login.UserMixin):
    pass

cfg = QPanelConfig()
backend = Backend()


def get_data_queues(queue=None):
    data = backend.get_data_queues()
    if queue is not None:
        try:
            data = data[queue]
        except:
            abort(404)
    if cfg.is_debug:
        app.logger.debug(data)
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
APPLICATION_ROOT = cfg.base_url
app = Flask(__name__)
app.config.from_object(__name__)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = cfg.language
app.secret_key = cfg.secret_key

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

    if not cfg.has_users():
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
    if not cfg.has_users():
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


# Utilities helpers
@app.context_processor
def utility_processor():
    # Deprecated function
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
        return (cfg.interval * 1000)
    return dict(request_interval=request_interval)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.context_processor
def utility_processor():
    def check_upgrade():
        return cfg.check_upgrade
    return dict(check_upgrade=check_upgrade)


@app.context_processor
def utility_processor():
    def show_service_level():
        return cfg.show_service_level
    return dict(show_service_level=show_service_level)


@app.context_processor
def utility_processor():
    def has_users():
        return cfg.has_users()
    return dict(has_users=has_users)


@app.context_processor
def utility_processor():
    def clean_str_to_div_id(value):
        return uqpanel.clean_str_to_div_id(value)
    return dict(clean_str_to_div_id=clean_str_to_div_id)


@app.context_processor
def utility_processor():
    def is_freeswitch():
        return backend.is_freeswitch()
    return dict(is_freeswitch=is_freeswitch)


# ---------------------
# ---- Routes ---------
# ---------------------
# home
@app.route('/')
@flask_login.login_required
def home():
    data = get_data_queues()
    template = 'index.html'
    if backend.is_freeswitch():
        template = 'fs/index.html'
    return render_template(template, queues=data)


@app.route('/queue/<name>')
@flask_login.login_required
def queue(name=None):
    data = get_data_queues(name)
    template = 'queue.html'
    if backend.is_freeswitch():
        template = 'fs/queue.html'
    return render_template(template, data=data, name=name)


@app.route('/queue/<name>.json')
@flask_login.login_required
def queue_json(name=None):
    data = get_data_queues(name)
    return jsonify(name=name, data=data)


# data queue
@app.route('/queues')
@flask_login.login_required
def queues():
    data = get_data_queues()
    return jsonify(data=data)


@app.route('/lang')
@app.route('/lang/<language>')
@flask_login.login_required
def language(language=None):
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
        require_upgrade=need_upgrade,
        current_version=get_current_version(),
        last_stable_version=get_stable_version()
    )


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

# ---------------------
# ---- Main  ----------
# ---------------------
if __name__ == '__main__':

    if cfg.is_debug:
        app.config['DEBUG'] = True

    if APPLICATION_ROOT == '/':
        app.run(host=cfg.host_bind, port=cfg.port_bind, use_reloader=True,
                extra_files=[cfg.path_config_file])
    else:
        application = DispatcherMiddleware(Flask('dummy_app'), {
            app.config['APPLICATION_ROOT']: app,
        })
        run_simple(cfg.host_bind, cfg.port_bind, application,
                   use_reloader=True, extra_files=[cfg.path_config_file])
