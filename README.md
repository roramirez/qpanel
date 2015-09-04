# Qpanel

Qpanel is dashboard for Queues in Asterisk

![Demo](samples/animation.gif)

## Requirement
 * Python 2.6+
 * [Flask](http://flask.pocoo.org/) 0.10+
 * [Asterisk](http://www.asterisk.org) 1.4+ and enabled manager

 If you used a CentOS 5.X or Elastix check [how to install Python 2.6 and Flask](README.Centos5.md)

## 1. Install flask
```
 $ pip install Flask
```
If dont have pip in your system. For install

### Debian and Ubuntu
 ```
 sudo apt-get install python-pip
 ```

### Fedora
 ```
 sudo yum install python-pip
 ```


## 2. Clone this repository
```
 git clone -b stable  https://github.com/roramirez/qpanel.git
```
##  3. Go and prepair environment
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

If you want check the development version get checkout to master branch

 ```
 git clone -b master  https://github.com/roramirez/qpanel.git
 ```
