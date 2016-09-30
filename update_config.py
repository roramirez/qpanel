# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

from qpanel import utils
import sys

if __name__ == '__main__':
    sections = ['general', 'manager', 'rename', 'users']
    file_config = sys.argv[1].strip()
    file_template = sys.argv[2].strip()
    utils.unified_configs(file_config, file_template, sections)
