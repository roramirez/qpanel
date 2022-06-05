# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2022 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#
from __future__ import absolute_import
import six.moves.configparser
import os
from distutils.util import strtobool
from .convert import convert_time_when_param
import six


class NotConfigFileQPanel(BaseException):
    '''
        This exception is raised when is not possible read file for
        QPanel config.
    '''

    def __init__(self, file_path):
        error = 'Error to open file config. Check if %s file exist' % file_path
        super(NotConfigFileQPanel, self).__init__(error)


class QPanelConfig:

    def __init__(self, path_config_file=None):
        if path_config_file:
            self.path_config_file = path_config_file
        else:
            dirname, filename = os.path.split(os.path.abspath(__file__))
            config_file_path = os.path.join(dirname, os.pardir, 'config.ini')
            # Enable set by enviroment varible the path for configuracion file
            # This can be useful to test suite and when is running by process
            # manager like supervisor, wsgi, circus, etc..
            self.path_config_file = os.environ.setdefault(
                'QPANEL_CONFIG_FILE', config_file_path)

        self.config = self.__open_config_file(self.path_config_file)

        # properties
        self.is_debug = self.__get_bool_value_config('general', 'debug', False)
        self.port_bind \
            = int(self.__get_entry_ini_default('general', 'port', 5000))
        self.host_bind \
            = self.__get_entry_ini_default('general', 'host', '0.0.0.0')
        self.base_url \
            = self.__get_entry_ini_default('general', 'base_url', '/')
        self.language \
            = self.__get_entry_ini_default('general', 'language', 'en')
        self.secret_key \
            = self.__get_entry_ini_default('general', 'secret_key',
                                           'CHANGEME_ON_CONFIG')
        self.interval \
            = self.__get_entry_int_min_value('general', 'interval', 1)
        self.check_upgrade \
            = self.__get_bool_value_config('general', 'check_upgrade', True)
        self.show_service_level \
            = self.__get_bool_value_config('general',
                                           'show_service_level', False)
        self.theme = self.get_theme()

    def __open_config_file(self, file_path):
        cfg = six.moves.configparser.ConfigParser()
        try:
            with open(file_path) as f:
                if six.PY3:
                    cfg.read_file(f)
                else:
                    cfg.readfp(f)
                return cfg
        except IOError:
            raise NotConfigFileQPanel(file_path)

    def get_hide_config(self):
        tmp = self.__get_entry_ini_default('general', 'hide', '')
        tmp = tmp.replace('\'', '')
        return [s.strip() for s in tmp.split(',')]

    def get_show_config(self):
        ''' Get show config from config.ini '''
        tmp = self.__get_entry_ini_default('general', 'show', '')
        tmp = tmp.replace('\'', '')
        tmp = [s.strip() for s in tmp.split(',')]
        return[s for s in tmp if len(s) >= 1]

    def __get_entry_ini_default(self, section, var, default):
        try:
            var = self.config.get(section, var)
            v = var
        except:
            return default
        return v

    def __get_bool_value_config(self, section, option, default):
        try:
            var = self.config.get(section, option)
            v = True if strtobool(var) == 1 else False
        except:
            return default
        return v

    def __get_entry_int_min_value(self, section, option, min=0):
        v = int(self.__get_entry_ini_default(section, option, min))
        if v < min:
            return min
        return v

    def get(self, section, var):
        return self.config.get(section, var)

    def get_value_set_default(self, section, var, default):
        return self.__get_entry_ini_default(section, var, default)

    def count_element_sections_config(self, section, cfg=None):
        try:
            if not cfg:
                cfg = self.config
            return len(dict(cfg.items(section)))
        except:
            return 0

    def has_users(self):
        return self.has_section('users')

    def has_user_queues(self):
        return self.has_section('user_queues')

    def enable_queue_for_user(self, username, queuename):
        if self.has_user_queues() is False:
            return True
        return queuename in self.queue_enables_for_username(username)

    def queue_enables_for_username(self, username):
        queues = []
        user_configs = self.get_items('user_queues')
        if user_configs is None:
            return []
        user_configs = dict(user_configs)
        if username in user_configs.keys():
            tmp = user_configs[username]
            tmp = tmp.replace('\'', '')
            tmp = [s.strip() for s in tmp.split(',')]
            queues = [s for s in tmp if len(s) >= 1]
        return queues

    def has_queuelog_config(self):
        return self.has_section('queue_log')

    def has_section(self, section):
        if self.count_element_sections_config(section, self.config) > 0:
            return True
        return False

    def is_freeswitch(self):
        return self.__get_bool_value_config('general', 'freeswitch', False)

    def queues_for_reset_stats(self):
        values = {}
        if self.count_element_sections_config('reset_stats', self.config) > 0:
            elements = self.config.items('reset_stats')
            for queue, v in elements:
                values[queue] = convert_time_when_param(v)
        return values

    def get_items(self, section):
        try:
            return self.config.items(section)
        except BaseException:
            return None

    def get_theme(self):
        """
            get the theme from configuration.
            only one from available_themes
            if not match return default theme
        """
        available_themes = ['qpanel', 'old']
        theme = self.__get_entry_ini_default('general', 'theme', 'qpanel')
        theme = theme.lower()
        if theme not in available_themes:
            return 'qpanel'
        return theme

    def realname_queue(self, queuename):
        """
        Return the realname for a queue if this is using a rename
        from config.ini [rename] section

        param str queuename: The name of queue (renamed)
        """
        renames = self.get_items('rename')
        if renames is not None:
            for val, idx in renames:
                if idx == queuename:
                    return val
        return queuename
