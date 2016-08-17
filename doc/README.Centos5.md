# Centos 5

If you OS. is Centos 5.X with EPEL repository activated this guide show how to install install Flask and Python 2.6.

If you prefered install [Python from source read this guide] (Python26Source.md)


## Python and PIP
```
yum install python26 python26-devel
wget --no-check-certificate  https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
python2.6 /tmp/get-pip.py

```



## Flask
Will be use pip2.6 for install Flask and dependencies

```
pip2.6 install -r requirements.txt
```
