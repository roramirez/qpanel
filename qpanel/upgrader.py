# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

import requests
from distutils.version import LooseVersion
import qpanel


BRANCH = 'stable'
REPO = 'git@github.com:roramirez/qpanel.git'
URL_STABLE_VERSION = 'https://rodrigoramirez.com/qpanel/version/' + BRANCH


def require_upgrade():
    return check_require_upgrade(get_current_version(), get_stable_version())


def check_require_upgrade(current, stable):
    a = LooseVersion(current)
    b = LooseVersion(stable)
    if a < b:
        return True
    return False


# InmplementME
def last_check_update():
    return True


def get_current_version():
    return qpanel.__version__


def get_stable_version(url=URL_STABLE_VERSION):
    stable_version = __get_data_url(url)
    return __first_line(stable_version)


def __get_data_url(url):
    req = requests.get(url)
    try:
        return req.text
    except:
        return None


def __first_line(content):
    tmp = ''
    if content is not None:
        tmp = content.splitlines()
    if len(tmp) >= 1:
        return tmp[0]
    return tmp
