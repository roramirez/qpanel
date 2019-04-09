#!/bin/bash


case $RUN in

     flake8)
         # We'll need remote 'git diff' part when all lint error are fixed.
         git remote set-branches origin 'develop'
         git fetch --depth 1 origin develop
         git diff origin/develop | flake8 --diff --ignore=E121,E123,E126,E133,E226,E241,E242,E402,E704 .
          ;;
     tox)
          docker run -it --rm --name qpanel-tox -v $(pwd):/code n42org/tox bash -c 'apt-get update; apt-get install -y swig build-essential; cd /code; tox'
          ;;

esac
