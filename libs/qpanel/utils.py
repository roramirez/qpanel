# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

from __future__ import absolute_import
import six.moves.configparser
from datetime import timedelta, date, datetime
import time
from .config import QPanelConfig
import calendar


def unified_configs(file_config, file_template, sections=[]):

    config = QPanelConfig(file_config).config
    template = QPanelConfig(file_template).config

    # create new file based in template
    for s in sections:
        items = dict(template.items(s))
        for i in items:
            try:
                template.set(s, i, config.get(s, i))
            except:
                pass

    # set old configs
    for s in config.sections():
        items = dict(config.items(s))
        for i in items:
            try:
                template.set(s, i, config.get(s, i))
            except six.moves.configparser.NoSectionError:
                template.add_section(s)
                template.set(s, i, config.get(s, i))

    file = open(file_config, 'wr')
    template.write(file)
    file.close()


# http://stackoverflow.com/a/6425628
def underscore_to_camelcase(word):
    """
        Convert word to camelcase format
    """
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def clean_str_to_div_id(value):
    """ Clean String for a div name.
        Convert character like @ / and . for more easy use in JQuery
        Parameter: value = string
    """
    v = value.replace('/', '-')
    v = v.replace('.', '_')
    return v.replace('@', '_')


def timedelta_from_field_dict(field, dic, current_timestamp=None,
                              is_seconds_ago=False):
    seconds_ago = 0
    if not current_timestamp:
        current_timestamp = time.time()
    if field in dic:
        if int(dic[field]) > 0:
            if is_seconds_ago:
                seconds_ago = int(dic[field])
            else:
                seconds_ago = int(current_timestamp) - int(dic[field])

    return timedelta(seconds=seconds_ago)


def first_data_dict(data):
    if data:
        return list(data.keys())[0]
    else:
        return ''


def init_day(d=None):
    if d is None:
        d = date.today()
    return datetime(d.year, d.month, d.day, 0, 0, 0)


def end_day(d=None):
    if d is None:
        d = date.today()
    return datetime(d.year, d.month, d.day, 23, 59, 59)


# http://stackoverflow.com/a/13260981
# Convert a unix time u to a datetime object d, and vice versa
def dt(u):
    return datetime.utcfromtimestamp(u)


def ut(d):
    return calendar.timegm(d.timetuple())


def realname_queue_rename(queuename):
    renames = QPanelConfig().get_items('rename')
    if renames is not None:
        for val, idx in renames:
            if idx == queuename:
                return val
    return queuename

def add_debug_toolbar(app):
    try:
        from flask_debugtoolbar import DebugToolbarExtension
        toolbar = DebugToolbarExtension(app)
    except:
        pass
