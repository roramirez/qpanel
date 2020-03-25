# Guide to install QPanel in FusionPBX in Centos 7

This guide pretend enable the feature to match filter queue by user domain in FusionPBX. Also you could use for your custom proposes.

The steps starting with $ should be run a shell console as root user

Install a dependencies
----------------------

The next step you need install dependencies for ESL (swig) and virtualenv and uwsgi.


    $ yum install -y git python-virtualenv swig gcc gcc-c++ nodejs uwsgi uwsgi-plugin-python2


Enviroment setup
-----------------

Where the software is added. 

    $ mkdir /usr/local/apps
    $ cd /usr/local/apps
    $ git clone https://github.com/roramirez/qpanel.git
    $ cd qpanel
    $ git checkout domain-filter-fusion-pbx



Next steps are for install QPanel dependencies

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ pip install uwsgi
    $ npm install
    $ node_modules/bower/bin/bower --allow-root install


Copy the configuration sample file to use with Freeswitch

    $ cp samples/config.ini-dist config.ini

Set FreeSwitch as backend. This intruction replace comment line to use FS in the configuration file

    $ sed -ie 's/;freeswitch = True/freeswitch = True/g' config.ini
```
    $ echo '
[freeswitch]
host = 127.0.0.1
port = 8021
password = ClueCon
' >> config.ini
 ```
Use a external custom script to filter the queue for domain
    $ sed -i -E s/';external_login'/'external_login'/g config.ini 


```
$ echo '
[uwsgi]
socket= 0.0.0.0:5000
protocol=http
master = true
venv = /usr/local/apps/qpanel/env
chdir = /usr/local/apps/qpanel
mount = /qpanel=start.wsgi
manage-script-name = true
uid = freeswitch
gid = daemon
plugins = python
' > /usr/local/apps/qpanel/qpanel.ini
```

Create service qpanel for SystemV

```
$ echo '
[Unit]
Description=uWSGI instance to serve qpanel
After=network.target

[Service]
User=freeswitch
Group=daemon
WorkingDirectory=/usr/local/apps/qpanel/
Environment="PATH=/usr/local/apps/qpanel/env/bin"
ExecStart=/usr/local/apps/qpanel/env/bin/uwsgi --ini qpanel.ini


[Install]
WantedBy=multi-user.target' > /etc/systemd/system/qpanel.service

```



Add the follow lines in the file /etc/nginx/sites-enabled/fusionpbx.conf in the section for server ssl (443) just before the statement for 'location = /core/upgrade/index.php {' in the line 218


```
## Init Nginx Configuration ###

    location  /static {
        alias /usr/local/apps/qpanel/qpanel/static;
    }
    location  /_themes {
        alias /usr/local/apps/qpanel/qpanel/static;
    }
    location /qpanel {
        proxy_pass       http://localhost:5000/qpanel;
        proxy_set_header Host      $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
## End Nginx Configuration ###
```


Custom Configuration for FusionPBX
----------------------------------

The next step is add custom script to filter the queue for domain 

    $ cp samples/qpanel-fusionpbx4.php /var/www/fusionpbx/resources/qpanel.php


Open the /var/www/fusionpbx/themes/default/template.php and add the next content just above '            //domain name/selector' line 963

```
// Init menu content

            echo " <li class='nav-item dropdown '>
                <a class='nav-link'  href='/qpanel/login_external?domain_name=".$_SESSION['domain_name']."&domain_uuid=".$_SESSION['domain_uuid']."&username=".$_SESSION['username']."&user_uuid=".$_SESSION['user_uuid']."' >
                    <span class='fas fas fa-chart-pie' title='QPanel'></span>
                    <span class='d-sm-none d-md-none d-lg-inline' style='margin-left: 5px;'>QPanel</span>
                 </a>
               </li>";

// End menu content

```

Restart and enable services
---------------------------

    $ mkdir -p  /run/uwsgi/
    $ chown uwsgi:uwsgi /run/uwsgi
    $ chown freeswitch:daemon /etc/uwsgi.d/uwsgi-qpanel.ini
    $ systemctl enable qpanel
    $ systemctl start qpanel
    $ service nginx reload
