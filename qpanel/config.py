# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#
from __future__ import absolute_import
import six.moves.configparser
import os
from distutils.util import strtobool
from .convert import convert_time_when_param


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
        dirname, filename = os.path.split(os.path.abspath(__file__))
        if path_config_file:
            self.path_config_file = path_config_file
        else:
            self.path_config_file = os.path.join(dirname, os.pardir, 'config.ini')

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

    def __open_config_file(self, file_path):
        cfg = six.moves.configparser.ConfigParser()
        try:
            with open(file_path) as f:
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

    def has_queuelog_config(self):
        return self.has_section('queue_log')

    def has_section(self, section):
        v = False
        if self.count_element_sections_config(section, self.config) > 0:
            v = True
        return v

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
        except:
            return None
