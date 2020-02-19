##  Install on FreePBX 15 


This guide is thanks to @Mystic8b . You can see the #226 about this and also you can be better this Howto.



Install Dependencies

```
yum install -y git python-virtualenv swig mod_wsgi python-pip
cd /var/www
git clone https://github.com/roramirez/qpanel.git
cd qpanel
pip install -r requirements.txt
npm install
```

Prepare the  configurations for the deploy

```
cp samples/config.ini-dist config.ini
cp samples/configs/site-apache2-wsgi.conf /etc/httpd/conf.d/qpanel.conf
```

```
pybabel compile -d qpanel/translations
```


In **qpanel/config.ini** changed :
```
user = admin
password = from /etc/asterisk/maneger.conf
```

In **/etc/httpd/conf.d/qpanel.conf** changed :
```
ServerName yoursite.com
WSGIDaemonProcess app user=apache group=apache threads=1(or more)
#(You can create a virtual environment and add the path to it as it is written in the commented out config message)
ErrorLog /var/www/qpanel/logs/error.log
CustomLog /var/www/qpanel/logs/qpanel.access.log combined
```
And correct the rest of the path if necessary

In **/etc/httpd/conf/httpd.conf** add this line:
`WSGISocketPrefix /usr/ #Or something dir with 755`
I needed it because in the logs I got _"Unable to connect to WSGI daemon process"_

`#service httpd restart`

