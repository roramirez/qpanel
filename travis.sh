#!/bin/bash


case $RUN in

     flake8)
          flake8 --ignore=E121,E123,E126,E133,E226,E241,E242,E402,E704 .
          ;;
     tox)
          docker run -it --rm --name qpanel-tox -v $(pwd):/code n42org/tox bash -c 'cd /code ; tox'
          ;;

esac
