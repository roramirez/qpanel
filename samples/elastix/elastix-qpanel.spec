%define modname qpanel
Name:    elastix-%{modname}
Version: 0.3.0
Release: 2%{?dist}
Summary: Qpanel is dashboard for Queues in Asterisk
Group:   Applications/Communications
License: MIT
URL:     https://github.com/roramirez/qpanel
Source0: %{modname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{modname}-%{version}-root
Prereq: elastix-framework >= 2.2.0-25


Requires: python26 python26-devel nginx
BuildArch: noarch

%description
Qpanel is a dashboard for app_queue of Asterisk


%prep
%setup -n %{modname}-%{version}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/opt/%{modname}
mv * $RPM_BUILD_ROOT/opt/%{modname}
mkdir -p $RPM_BUILD_ROOT/usr/share/elastix/module_installer/%{name}-%{version}-%{release}/
cp $RPM_BUILD_ROOT/opt/%{modname}/samples/configs/elastix/menu.xml $RPM_BUILD_ROOT/usr/share/elastix/module_installer/%{name}-%{version}-%{release}/

%post
#Manager config
RAN_PASS=$(date +%s | sha256sum | base64 | head -c 32 ; echo)
cp /opt/%{modname}/config.ini-dist /opt/%{modname}/config.ini
sed -i "s/= password/= $RAN_PASS/" /opt/%{modname}/config.ini
sed -i "s/= username/= qpanel/" /opt/%{modname}/config.ini
sed -i "s/;base_url = /base_url =  \/qpanel/" /opt/%{modname}/config.ini
echo  "#include \"manager_qpanel.conf\"" >> /etc/asterisk/manager_additional.conf
echo "
[qpanel]
secret = $RAN_PASS
read = command
write = command
" > /etc/asterisk/manager_qpanel.conf

asterisk -rx "reload"


#Install pip
wget --no-check-certificate  https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
python2.6 /tmp/get-pip.py

#Flask
pip2.6 install flask

###### UWSGI  ##########
# install
pip2.6 install uwsgi

# config from repo
mkdir /etc/uwsgi
cp /opt/%{modname}/samples/configs/uwsgi-qpanel.ini /etc/uwsgi/
sed -i "s/venv/;venv/" /etc/uwsgi/uwsgi-qpanel.ini
sed -i "s/path\/app/opt\/qpanel/" /etc/uwsgi/uwsgi-qpanel.ini

# init.d 
echo '

#!/bin/bash

# uwsgi - Use uwsgi to run python and wsgi web apps.
#
# chkconfig: - 85 15
# description: Use uwsgi to run python and wsgi web apps.
# processname: uwsgi
# idea: https://www.linode.com/docs/websites/nginx/wsgi-using-uwsgi-and-nginx-on-centos-5


PATH=/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/bin/uwsgi

OWNER=uwsgi
NAME=uwsgi
DESC=uwsgi

UWSGI_EMPEROR_MODE=true
UWSGI_VASSALS="/etc/uwsgi/"

test -x $DAEMON || exit 0

# Include uwsgi defaults if available
if [ -f /etc/default/uwsgi ] ; then
    . /etc/default/uwsgi
fi

set -e

get_pid() {
    if [ -f /var/run/$NAME.pid ]; then
        echo `cat /var/run/$NAME.pid`
    fi
}

DAEMON_OPTS="-s 127.0.0.1:9001 -d /var/log/uwsgi.log --pidfile /var/run/$NAME.pid"


if [ "$UWSGI_EMPEROR_MODE" = "true" ] ; then
    DAEMON_OPTS="$DAEMON_OPTS --emperor $UWSGI_VASSALS"
fi

case "$1" in
  start)
        echo -n "Starting $DESC: "
        PID=$(get_pid)
        if [ -z "$PID" ]; then
            [ -f /var/run/$NAME.pid ] && rm -f /var/run/$NAME.pid

            touch /var/run/$NAME.pid
            #chown $OWNER /var/run/$NAME.pid
        $DAEMON $DAEMON_OPTS
        #su - $OWNER -pc "$DAEMON $DAEMON_OPTS"
        echo "$NAME."
        fi

    ;;
  stop)
       echo -n "Stopping $DESC: "
        PID=$(get_pid)
        [ ! -z "$PID" ] && kill -s 3 $PID &> /dev/null
        if [ $? -gt 0 ]; then
            echo "was not running"
            exit 1
        else
            echo "$NAME."
            rm -f /var/run/$NAME.pid &> /dev/null
        fi
     ;;
  reload)
        echo "Reloading $NAME"
        PID=$(get_pid)
        [ ! -z "$PID" ] && kill -s 1 $PID &> /dev/null
        if [ $? -gt 0 ]; then
            echo "was not running"
            exit 1
        else
            echo "$NAME."
            rm -f /var/run/$NAME.pid &> /dev/null
        fi
     ;;
  force-reload)
        echo "Reloading $NAME"
        PID=$(get_pid)
        [ ! -z "$PID" ] && kill -s 15 $PID &> /dev/null
        if [ $? -gt 0 ]; then
            echo "was not running"
            exit 1
        else
            echo "$NAME."
            rm -f /var/run/$NAME.pid &> /dev/null
        fi
        ;;
  restart)
        $0 stop
        sleep 2
        $0 start
       ;;
  status)
     killall -10 $DAEMON
     ;;
      *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop|restart|reload|force-reload|status}" >&2
        exit 1
        ;;
    esac
    exit 0
' > /etc/init.d/uwsgi

chmod +x /etc/init.d/uwsgi
chkconfig --add uwsgi
chkconfig uwsgi on
/etc/init.d/uwsgi start



#Nginx

echo '
server {
  listen   8081;
  server_tokens off;
  location = /qpanel { rewrite ^ /qpanel/; }
  location /qpanel { try_files $uri @qpanel; }
  location @qpanel {
    include uwsgi_params;
    uwsgi_param SCRIPT_NAME /qpanel;
    uwsgi_modifier1 30;
    uwsgi_pass unix:/tmp/qpanel.sock;
  }

}

' > /etc/nginx/conf.d/qpanel.conf

#Change por nginx
sed -i 's/listen\s*80;/listen 8080;/' /etc/nginx/nginx.conf
chkconfig nginx on
/etc/init.d/nginx start

# httpd apache

echo '
ProxyPass /qpanel http://127.0.0.1:8081/qpanel
<Location /qpanel>
        ProxyPassReverse /qpanel
        Order deny,allow
        Allow from all
</Location>
' > /etc/httpd/conf.d/qpanel.conf

/etc/init.d/httpd reload

pathModule="/usr/share/elastix/module_installer/%{name}-%{version}-%{release}"
# Run installer script to fix up ACLs and add module to Elastix menus.
elastix-menumerge $pathModule/menu.xml


%pre
mkdir -p /usr/share/elastix/module_installer/%{name}-%{version}-%{release}/


%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ $1 -eq 0 ] ; then # Validation for desinstall this rpm
    echo "Delete menus"
    elastix-menuremove "%{modname}"
fi

%files
%defattr(-,root,root,-)
/opt/%{modname}/*
/usr/share/elastix/module_installer/*
%doc

%changelog
