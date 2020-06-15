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

RUN apk add --ino-cache \
        git \
        py3-pip \
        npm \
        py3-babel \
        tini \
        swig \
        gcc \
        alpine-sdk \
        python3-dev && \
    cd / && \
    git clone \
        -b master \
        --depth=1 \
        https://github.com/roramirez/qpanel.git && \
    cd qpanel &&  \
    pip3 install -r requirements.txt && \
    cd /qpanel && \
    npm install && \
    cd /qpanel && \
    pybabel compile -d qpanel/translations && \
    cd /qpanel && \
    cp samples/config.ini-dist config.ini && \
    apk del --quiet \
        git \
        npm \
        gcc \
        alpine-sdk \
        python-dev

WORKDIR /qpanel

EXPOSE 5000

CMD [ ! -z "${QPANEL_USER}"   ] && \
    [ ! -z "${QPANEL_PWD}"    ] && \
    [ ! -z "${ASTERISK_HOST}" ] && \
       sed \
       -e "s/user = username/user = ${QPANEL_USER}/;s/password = password/password = ${QPANEL_PWD}/;s/host = localhost/host = ${ASTERISK_HOST}/" \
       -i config.ini; \
    tini -- python3 app.py