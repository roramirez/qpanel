# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

import ConfigParser
from datetime import timedelta, datetime
import time
from exception import NotConfigFileQPanel
import hashlib


def unified_configs(file_config, file_template, sections=[]):

    config = open_config_ini_file(file_config)
    template = open_config_ini_file(file_template)

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
            except ConfigParser.NoSectionError:
                template.add_section(s)
                template.set(s, i,  config.get(s, i))

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


def to_md5(val):
    m = hashlib.md5()
    m.update(val)
    return m.hexdigest()


def open_config_ini_file(file_path):
    cfg = ConfigParser.ConfigParser()
    try:
        with open(file_path) as f:
            cfg.readfp(f)
            return cfg
    except IOError:
        raise NotConfigFileQPanel(file_path)

def get_now():
    return datetime.now()
