# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

from config import QPanelConfig
from flask.ext.babel import format_timedelta
from datetime import timedelta
from  utils import timedelta_from_field_dict
import os
import sys

from libs.qpanel.asterisk import *
# In case use Asterisk dont crash with ESL not in system
try:
    from libs.qpanel.freeswitch import *
except:
    pass


class ConnectionErrorAMI(Exception):
    pass

class Backend(object):

    def __init__(self):
        self.config = QPanelConfig()

        section_config = 'freeswitch'
        if self.is_asterisk():
            section_config = 'manager'
            self.user = self.config.get(section_config, 'user')

        self.host = self.config.get(section_config, 'host')
        self.port = int(self.config.get(section_config, 'port'))
        self.password = self.config.get(section_config, 'password')

        self.connection = self._connect()

    def is_freeswitch(self):
        return self.config.is_freeswitch()

    def is_asterisk(self):
        return not self.is_freeswitch()

    def _connect(self):
        if self.is_freeswitch():
            return self._connect_esl()
        return self._connect_ami()

    def _connect_ami(self):
        manager = AsteriskAMI(self.host, self.port, self.user, self.password)
        return manager

    def _connect_esl(self):
        esl = Freeswitch(self.host, self.port, self.password)
        return esl

    def _get_data_queue_from_backend(self):
        self.connection = self._connect()
        try:
            return self.connection.queueStatus()
        except Exception, e:
            print str(e)
            return {}

    def get_data_queues(self):
        data = self._get_data_queue_from_backend()
        if self.is_freeswitch():
            return self.parse_fs(data)
        return self.parse_asterisk(data)

    def parse_data(self, data):
        data = self.hide_queue(data)
        data = self.rename_queue(data)
        if self.is_freeswitch():
            return self.parse_fs(data)
        return self.parse_asterisk(data)


    def parse_fs(self, data):
        for q in data:
            for m in data[q]['members']:
                member =  data[q]['members'][m]
                member['LastBridgeEndAgo'] = format_timedelta(timedelta_from_field_dict('LastBridgeEnd', member) , granularity='second')
                member['LastStatusChangeAgo'] = format_timedelta(timedelta_from_field_dict('LastStatusChange', member) , granularity='second')

            for c in data[q]['entries']:
                data[q]['entries'][c]['CreatedEpochAgo'] = format_timedelta(timedelta_from_field_dict('CreatedEpoch', data[q]['entries'][c]) , granularity='second')

        return data


    def parse_asterisk(self, data):
        # convert references manager to string
        for q in data:
            for e in data[q]['entries']:
                tmp = data[q]['entries'].pop(e)
                data[q]['entries'][str(e)] = tmp
                tmp = data[q]['entries'][str(e)]['Channel']
                data[q]['entries'][str(e)]['Channel']  = str(tmp)
            for m in data[q]['members']:
                member =  data[q]['members'][m]
                #Asterisk 1.8 dont have StateInterface
                if 'StateInterface' not in member:
                    member['StateInterface'] = m

                member['LastCallAgo'] = format_timedelta(timedelta_from_field_dict('LastCall', member) , granularity='second')
                # Time last pause
                member['LastPauseAgo'] = format_timedelta(timedelta_from_field_dict('LastPause', member) , granularity='second')

            for c in data[q]['entries']:
                data[q]['entries'][c]['WaitAgo'] = format_timedelta(timedelta_from_field_dict('Wait', data[q]['entries'][c], True) , granularity='second')


        return data


    def hide_queue(self, data):
        tmp_data = {}
        hide = config.get_hide_config()
        for q in data:
            if q not in hide:
                tmp_data[q] = data[q]
        return tmp_data


    def rename_queue(self, data):
        tmp_data = {}
        for q in data:
            rename = config.get_value_set_default('rename', q, None)
            if rename is not None:
                tmp_data[rename] = data[q]
            else:
                tmp_data[q] = data[q]
        return tmp_data

