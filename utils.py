# -*- coding: utf-8 -*-

#
# Copyright (C) 2015 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
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

    for s in sections:
        items =  dict(template.items(s))
        for i in items:
            try:
                template.set(s, i,  config.get(s, i))
            except:
                pass

    file = open(file_config, 'wr')
    template.write(file)
    file.close()
