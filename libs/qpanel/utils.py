# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

import ConfigParser
from datetime import timedelta, date, datetime
import time
import calendar


def unified_configs(file_config, file_template, sections=[]):
    f = open(file_config, 'r')
    config = ConfigParser.ConfigParser()
    config.readfp(f)
    f.close()

    f2 = open(file_template)
    template = ConfigParser.ConfigParser()
    template.readfp(f2)
    f2.close()

    # create new file based in template
    for s in sections:
        items = dict(template.items(s))
        for i in items:
            try:
                template.set(s, i,  config.get(s, i))
            except:
                pass

    # set old configs
    for s in config.sections():
        items = dict(config.items(s))
        for i in items:
            try:
                template.set(s, i,  config.get(s, i))
            except:
                pass

    file = open(file_config, 'wr')
    template.write(file)
    file.close()


# http://stackoverflow.com/a/6425628
def underscore_to_camelcase(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def clean_str_to_div_id(value):
    v = value.replace('/', '-')
    v = v.replace('.', '_')
    return v.replace('@', '_')


def timedelta_from_field_dict(field, dic, current_timestamp=None,
                              is_seconds_ago=False):
    second_ago = 0
    if not current_timestamp:
        current_timestamp = time.time()
    if field in dic:
        if int(dic[field]) > 0:
            if is_seconds_ago:
                seconds_ago = int(dic[field])
            else:
                second_ago = int(current_timestamp) - int(dic[field])

    return timedelta(seconds=second_ago)


def first_data_dict(data):
    if data:
        return data.keys()[0]
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
