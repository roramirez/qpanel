%define modname qpanel
Name:    elastix-%{modname}
Version: 0.13.1
Release: 1%{?dist}
Summary: Qpanel is dashboard for Queues in Asterisk
Group:   Applications/Communications
License: MIT
URL:     https://github.com/roramirez/qpanel
Source0: %{modname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{modname}-%{version}-root
Prereq: elastix-framework >= 4.0.0


Requires: httpd, python >= 2.7, python-pip, mod_wsgi, git
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
cp $RPM_BUILD_ROOT/opt/%{modname}/samples/elastix/menu.xml $RPM_BUILD_ROOT/usr/share/elastix/module_installer/%{name}-%{version}-%{release}/

%post



CONFIG_FILE=/opt/%{modname}/config.ini
if ! [ -f "$CONFIG_FILE" ]; then

  #Manager config
  RAN_PASS=$(date +%s | sha256sum | base64 | head -c 32 ; echo)
  cp /opt/%{modname}/samples/config.ini-dist /opt/%{modname}/config.ini
  sed -i "s/= password/= $RAN_PASS/" /opt/%{modname}/config.ini
  sed -i "s/= username/= qpanel/" /opt/%{modname}/config.ini
  sed -i "s/;base_url = /base_url =  \/qpanel/" /opt/%{modname}/config.ini

  search_include=$(grep  manager_qpanel.conf /etc/asterisk/manager.conf | grep  -v ';')
  if  [ ${#search_include} -eq 0 ]; then
    echo  "#include manager_qpanel.conf" >> /etc/asterisk/manager.conf;
  fi

echo "
[qpanel]
secret = $RAN_PASS
read = command
write = command
" > /etc/asterisk/manager_qpanel.conf

else
  python /opt/%{modname}/update_config.py $CONFIG_FILE /opt/%{modname}/samples/config.ini-dist
fi


asterisk -rx "reload"


# Dependencies
pip install virtualenv
mkdir /opt/%{modname}/env
virtualenv  /opt/%{modname}/env
source /opt/%{modname}/env/bin/activate
pip install -r /opt/%{modname}/requirements.txt
deactivate


# httpd apache
if ! [ -f "/etc/httpd/conf.d/qpanel.conf" ]; then
echo '
Alias /qpanel/static /opt/qpanel/static
<Directory /opt/qpanel/static>
    Require all granted
</Directory>

<Directory /opt/qpanel>
    <Files start.wsgi>
        Require all granted
    </Files>
</Directory>

WSGISocketPrefix /var/run/wsgi
WSGIDaemonProcess qpanel_app python-path=/opt/qpanel:/opt/qpanel/env/lib/python2.7/site-packages
WSGIProcessGroup qpanel_app
WSGIScriptAlias /qpanel /opt/qpanel/start.wsgi process-group=qpanel_app
' > /etc/httpd/conf.d/qpanel.conf

service httpd restart
fi


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
