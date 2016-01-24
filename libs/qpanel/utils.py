# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

import ConfigParser

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

# http://stackoverflow.com/a/6425628
def underscore_to_camelcase(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))
