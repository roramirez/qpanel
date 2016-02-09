# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

import ConfigParser
from datetime import timedelta
import time

def unified_configs(file_config, file_template, sections = []):
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
        items =  dict(template.items(s))
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

def count_element_sections_config(section, cfg):
    try:
        return len(dict(cfg.items(section)))
    except:
        return 0

def timedelta_from_field_dict(field, dic, current_timestamp = time.time()):
    second_ago = 0
    if field in dic:
        if int(dic[field]) > 0:
            second_ago = int(current_timestamp) - int(dic[field])
    return timedelta(seconds=second_ago)
