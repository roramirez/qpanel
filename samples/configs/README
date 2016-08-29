# Configs samples

There some samples configs.


## AMI
manager_asterisk.conf: Example config for Asterisk manager for used with QPanel


## Nginx or Apache + UWSGI

If you like deploy system like a service without run like python app.py

Can you use a Nginx + UWSGI

There configs samples:

 * site-nginx.config: Virtualhost config for Nginx
 * site-apache2.conf: Virtualhost configuration for Apache2
 * uwsgi-qpanel.ini: Config app into uwsgi, some times you need add into /etc/uwsgi/apps-enabled


## Apache2 + WSGI
 * site-apache2-wsgi.conf: Virtualhost config for Apache using wsgi script

### Trouble?

### No plugin loaded
You have  error like:

```

Fri Aug 26 22:00:12 2016 - *** Operational MODE: preforking ***
Fri Aug 26 22:00:12 2016 - *** no app loaded. going in full dynamic mode ***
Fri Aug 26 22:00:12 2016 - *** uWSGI is running in multiple interpreter mode ***
Fri Aug 26 22:00:12 2016 - !!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!!
Fri Aug 26 22:00:12 2016 - no request plugin is loaded, you will not be able to manage requests.
Fri Aug 26 22:00:12 2016 - you may need to install the package for your language of choice, or simply load it with --plugin.

```

Some distros have package named uwsgi-plugin-python. You'll need install it
