%define modname qpanel

Name:           issabel-%{modname}
Version:        0.15.0
Release:        1
Summary:        Qpanel is dashboard for Queues in Asterisk
Group:          Applications/Communications
License:        MIT
URL:            https://github.com/roramirez/qpanel
Source0:        %{modname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch

Requires(pre):  issabel-framework >= 2.4.0-1

BuildRequires:  npm
BuildRequires:  python-babel >= 2.6

Requires:       issabelPBX >= 2.11
Requires:       mod_wsgi >= 3.4
Requires:       py-Asterisk >= 0.5
Requires:       python >= 2.7
Requires:       python-babel >= 2.6
Requires:       python-flask >= 0.10
Requires:       python-flask-babel >= 0.9
Requires:       python-flask-login >= 0.3
Requires:       python-redis >= 2.10
Requires:       python-rq >= 0.11
Requires:       python-rq-scheduler >= 0.6

%description
Qpanel is a dashboard for app_queue of Asterisk

%prep
%setup -n %{modname}-%{version}

%install
rm -rf %{buildroot}

# install js and css files
npm install

# translations
pybabel compile -d qpanel/translations

# The following folder should contain all the data that is required by the installer,
# that cannot be handled by RPM.
mkdir -p    %{buildroot}/usr/share/issabel/module_installer/%{name}-%{version}-%{release}/
mv samples/issabel/menu.xml %{buildroot}/usr/share/issabel/module_installer/%{name}-%{version}-%{release}/

# copy qpanel files
mkdir -p %{buildroot}/opt/%{modname}
mv * %{buildroot}/opt/%{modname}

%post

# Run installer script to fix up ACLs and add module to Issabel menus.
issabel-menumerge /usr/share/issabel/module_installer/%{name}-%{version}-%{release}/menu.xml

CONFIG_FILE=/opt/%{modname}/config.ini
if ! [ -f "$CONFIG_FILE" ]; then

  # Manager config
  RAN_PASS=$(date +%s | sha256sum | base64 | head -c 32 ; echo)
  cp /opt/%{modname}/samples/config.ini-dist /opt/%{modname}/config.ini
  sed -i "s/= password/= $RAN_PASS/" /opt/%{modname}/config.ini
  sed -i "s/= username/= qpanel/" /opt/%{modname}/config.ini
  sed -i "s/;base_url = /base_url =  \/qpanel/" /opt/%{modname}/config.ini

  search_include=$(grep  manager_qpanel.conf /etc/asterisk/manager.conf | grep  -v ';')
  if  [ ${#search_include} -eq 0 ]; then
    echo  "#include manager_qpanel.conf" >> /etc/asterisk/manager.conf;
  fi
else
  RAN_PASS=$(grep  "\[manager\]" -a5  $CONFIG_FILE | grep password | cut -f 3 --delimiter=" ")
  python /opt/%{modname}/update_config.py $CONFIG_FILE /opt/%{modname}/samples/config.ini-dist
fi

# Update or create manager config for qpanel user
CONFIG_FILE_MANAGER=/etc/asterisk/manager_qpanel.conf
if ! [ -f "$CONFIG_FILE_MANAGER" ]; then
  cp /opt/%{modname}/samples/configs/manager_asterisk.conf  $CONFIG_FILE_MANAGER
else
  # update role commands
  ROL_READ=$(grep  "read.*"   /opt/%{modname}/samples/configs/manager_asterisk.conf)
  ROL_WRITE=$(grep  "write.*"   /opt/%{modname}/samples/configs/manager_asterisk.conf)
  sed -i "s/read.*/$ROL_READ/" $CONFIG_FILE_MANAGER
  sed -i "s/write.*/$ROL_WRITE/" $CONFIG_FILE_MANAGER
fi
sed -i "s/secret.*/secret = $RAN_PASS/" $CONFIG_FILE_MANAGER
asterisk -rx "reload"

# httpd apache
if ! [ -f "/etc/httpd/conf.d/qpanel.conf" ]; then
echo '
Alias /qpanel/static /opt/qpanel/qpanel/static
<Directory /opt/qpanel/qpanel/static>
    Require all granted
</Directory>

WSGIScriptAlias /qpanel /opt/qpanel/start.wsgi
WSGIScriptReloading On

<Directory /opt/qpanel>
    Order deny,allow
    Allow from all

   <Files start.wsgi>
        Require all granted
    </Files>

</Directory>


' > /etc/httpd/conf.d/qpanel.conf

fi
service httpd restart

%pre
mkdir -p /usr/share/qpanel/module_installer/%{name}-%{version}-%{release}/


%clean
rm -rf %{buildroot}

%preun
if [ $1 -eq 0 ] ; then # Validation for desinstall this rpm

    # Remove qpanel from Issabel menu 
    issabel-menuremove %{modname}

    # remove apache config file
    if [ -f "/etc/httpd/conf.d/qpanel.conf" ]; then
      rm -f /etc/httpd/conf.d/qpanel.conf
      service httpd restart
    fi

    # Remove qpanel config
    CONFIG_FILE=/opt/%{modname}/config.ini
    if [ -f "$CONFIG_FILE" ]; then
      rm -f $CONFIG_FILE
    fi

    # remove config from asterisk
    search_include=$(grep manager_qpanel.conf /etc/asterisk/manager.conf | grep  -v ';')
    if  [ ${#search_include} -ne 0 ]; then
      sed -i 's/#include manager_qpanel\.conf//g' /etc/asterisk/manager.conf
    fi
    if [ -f "/etc/asterisk/manager_qpanel.conf" ]; then
      rm -f /etc/asterisk/manager_qpanel.conf
    fi
    asterisk -rx "reload"

fi

%files
%defattr(-, root, root)
%{_datadir}/issabel/module_installer/*
%defattr(-, asterisk, asterisk)
/opt/%{modname}

%doc

%changelog
