from urllib2 import Request, urlopen
from distutils.version import LooseVersion

BRANCH='stable'
REPO='git@github.com:roramireiz/qpanel.git'
URL_STABLE_VERSION='https://raw.githubusercontent.com/roramirez/qpanel/%s/VERSION' % BRANCH

def upgrader():
    return True

def require_upgrade():
    a = LooseVersion(get_current_version())
    b = LooseVersion(get_stable_version())
    if a < b:
        return True
    return False

def last_check_update():
    return True

def get_current_version():
    current_version = open('VERSION')
    return __first_line(current_version.read())

def get_stable_version():
    stable_version = __get_data_url(URL_STABLE_VERSION)
    return __first_line(stable_version)

def __get_data_url(url):
    req = Request(url)
    response = urlopen(req)
    return response.read()

def __first_line(content):
    tmp = content.split('\n')
    if len(tmp) > 1:
        return tmp[0]
    return tmp


# Test
print "stable version %s" %  get_stable_version()
print "current version %s" % get_current_version()
print "require upgrade? %s" % require_upgrade()
