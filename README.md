# Qpanel

Qpanel is dashboard for Queues in Asterisk

# Use
QPanel used [Flask](http://flask.pocoo.org/)

## 1. Install flask
```
 $ pip install Flask
```
If dont have pip in your system. For install

 ##### Debian and Ubuntu
 ```
 sudo apt-get install python-pip
 ```

 ##### Fedora
 ```
 sudo yum install python-pip
 ```


## 2. Clone this repo
```
 git clone -b stable  https://github.com/roramirez/qpanel.git
```
##  3. Go and prepair env
 ```
  cd qpanel
  git submodule init
  git submodule update
  cp config.ini-dist config.ini
 ```
  Edit config.ini with Manager Asterisk parameters

## 4.- Run and relax
 ```
    python app.py
 ```

Go url of machine http://IP:5000

## New features?
If you like new features or something is wrong [please open a issue](https://github.com/roramirez/qpanel/issues/new)
