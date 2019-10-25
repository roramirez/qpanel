#
# This file for Docker is thanks by @litnimax
# Is adapted to use Python 3 (The support for Python 2 was removed)
# You can find about this in https://github.com/roramirez/qpanel/issues/195
# If have any improved about this add a Pull Request o Issue.
#
# Maybe using a docker-compose would be fine in the future. Only add this in QPanel for
# for all dockerized users around the all shipping containers in the world.
#
# Chile in state of emergency, October 2019

FROM alpine:3.8

RUN apk add --ino-cache git py3-pip npm py3-babel tini swig gcc alpine-sdk python3-dev

RUN cd / && git clone -b master --depth=1 https://github.com/roramirez/qpanel.git && \
    cd qpanel &&  pip3 install -r requirements.txt

RUN cd /qpanel && npm install

RUN cd /qpanel && pybabel compile -d qpanel/translations

RUN cd /qpanel && cp samples/config.ini-dist config.ini

WORKDIR /qpanel

CMD tini -- python3 app.py

