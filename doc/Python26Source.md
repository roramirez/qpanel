# Python 2.6+ from source

If you a OS with a older than 2.6 version of Python necessary for QPanel because use Flask. This document show how to install from source Python 2.6 and Flask.

## Dependences
Minimal necessary compiler and openssl

### Based in RPM like RedHat, CentOS, Fedora, etc..

```
  yum install gcc cc
  yum install openssl-devel

```

## Python
Install Python from source

```
wget https://www.python.org/ftp/python/2.6.9/Python-2.6.9.tgz
tar -zxvf Python-2.6.9.tgz
cd Python-2.6.9
./configure && make && make install
```


## PIP
```
wget --no-check-certificate  https://bootstrap.pypa.io/get-pip.py
python2.6 get-pip.py

```

## Flask
Will be use pip2.6 for install Flask and dependences

```
 $ pip2.6 install -r requirements.txt

```
