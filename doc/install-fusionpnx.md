## How to FusionPBX in Centos 7


Here a little guide to deploy QPanel in a Centos 7 with FusionPBX

### Install a dependencies

The next step you need install dependencies for ESL (swig) and virtualenv and uwsgi


`yum install -y git  python-virtualenv swig gcc gcc-c++ nodejs uwsgi uwsgi-plugin-python2`


### Enviroment setup

Where you add software

```
    mkdir /usr/local/apps
    cd /usr/local/apps
    git clone https://github.com/roramirez/qpanel.git
```


Setup QPanel
```

    cd qpanel
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    npm install
    node_modules/bower/bin/bower --allow-root install
```

Configuration file

`cp samples/config.ini-dist config.ini`


Use a Freeswitch as Backend
```
 sed -ie 's/;freeswitch = True/freeswitch = True/g' config.ini

 echo '
[freeswitch]
host = 127.0.0.1
port = 8021
password = ClueCon
' >> config.ini

```

### Setup SO

Permissions
`chown freeswitch:daemon /usr/local/apps/qpanel`


Add uwsgi configuration

```
    echo '
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
' > /etc/uwsgi.d/uwsgi-qpanel.ini
```

Add this next line inside a HTTPs configuration in Nginx (/etc/nginx/sites-enabled/fusionpbx)


```
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
```

                                                                '
USWGI Setup


```
    mkdir -p  /run/uwsgi/
    chown uwsgi:uwsgi /run/uwsgi
    chown freeswitch:daemon /etc/uwsgi.d/uwsgi-qpanel.ini
    systemctl enable uwsgi
    systemctl start uwsgi
```
