# -*- coding: utf-8 -*-

#
# Copyright (C) 2015 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

import utils
import sys

if __name__ == '__main__':
    sections = ['general', 'manager', 'rename']
    file_config = sys.argv[1].strip()
    file_template = sys.argv[2].strip()
    utils.unified_configs(file_config, file_template, sections)
