# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#
import time


def convert_time_when_param(value, splitter=','):
    """ Convert string value to dict for time config for reset stats
    value = daily,00:10:50 -> return {'when': 'daily', 'hour': '00:10:50'}
    """
    var = value.split(splitter)
    hour = '00:00:00'
    if len(var) > 1:
        hour = var[1].strip()
    try:
        hour = time.strptime(hour, "%H:%M:%S")
    except ValueError:
        hour = time.strptime('00:00:00', "%H:%M:%S")
    hour = time.strftime('%M:%M:%S', hour)
    return {'when': var[0], 'hour': hour}
