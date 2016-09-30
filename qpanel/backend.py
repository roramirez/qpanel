# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

from __future__ import absolute_import
from __future__ import print_function
from .config import QPanelConfig
from flask_babel import format_timedelta
from .utils import timedelta_from_field_dict, realname_queue_rename
from .asterisk import *
import six
# In case use Asterisk dont crash with ESL not in system
try:
    from .freeswitch import *
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
        except Exception as e:
            print(str(e))
            return {}

    def get_data_queues(self):
        data = self._get_data_queue_from_backend()
        return self.parse_data(data)

    def parse_data(self, data):
        data = self.hide_queue(data)
        data = self.rename_queue(data)
        if self.is_freeswitch():
            return self.parse_fs(data)
        return self.parse_asterisk(data)

    def parse_fs(self, data):
        for q in data:
            for m in data[q]['members']:
                member = data[q]['members'][m]
                member['LastBridgeEndAgo'] = format_timedelta(
                    timedelta_from_field_dict('LastBridgeEnd', member),
                    granularity='second')
                member['LastStatusChangeAgo'] = format_timedelta(
                    timedelta_from_field_dict('LastStatusChange', member),
                    granularity='second')

            for c in data[q]['entries']:
                data[q]['entries'][c]['CreatedEpochAgo'] = format_timedelta(
                    timedelta_from_field_dict('CreatedEpoch',
                                              data[q]['entries'][c]),
                    granularity='second')

        return data

    def parse_asterisk(self, data):
        # convert references manager to string
        for q in data:
            for e in data[q]['entries']:
                tmp = data[q]['entries'].pop(e)
                data[q]['entries'][str(e)] = tmp
                tmp = data[q]['entries'][str(e)]['Channel']
                data[q]['entries'][str(e)]['Channel'] = str(tmp)
            for m in data[q]['members']:
                member = data[q]['members'][m]
                # Asterisk 1.8 dont have StateInterface
                if 'StateInterface' not in member:
                    member['StateInterface'] = m

                member['LastCallAgo'] = format_timedelta(
                    timedelta_from_field_dict('LastCall', member),
                    granularity='second')
                # Time last pause
                member['LastPauseAgo'] = format_timedelta(
                    timedelta_from_field_dict('LastPause', member),
                    granularity='second')

                # introduced in_call flag
                # asterisk commit 90b06d1a3cc14998cd2083bd0c4c1023c0ca7a1f
                if 'InCall' in member and member['InCall'] == '1':
                    member['Status'] = '10'

            for c in data[q]['entries']:
                data[q]['entries'][c]['WaitAgo'] = format_timedelta(
                    timedelta_from_field_dict('Wait',
                                              data[q]['entries'][c], True),
                    granularity='second')

        return data

    def hide_queue(self, data):
        tmp_data = {}
        hide = self.config.get_hide_config()
        show = self.config.get_show_config()
        if len(show) == 0:
            for q in data:
                if q not in hide:
                    tmp_data[q] = data[q]
        else:
            s = set(show)
            inter = s & six.viewkeys(data)
            tmp_data = {x:data[x] for x in inter if x in data}

        return tmp_data

    def rename_queue(self, data):
        tmp_data = {}
        for q in data:
            rename = self.config.get_value_set_default('rename', q, None)
            if rename is not None:
                tmp_data[rename] = data[q]
            else:
                tmp_data[q] = data[q]
        return tmp_data

    def _call_spy(self, channel, to_exten, with_whisper=False):
        self.connection = self._connect()
        try:
            return self.connection.spy(channel, to_exten, with_whisper)
        except Exception as e:
            print(str(e))
            return {}

    def whisper(self, channel, to_exten):
        return self._call_spy(channel, to_exten, 'w')

    def spy(self, channel, to_exten):
        return self._call_spy(channel, to_exten)

    def barge(self, channel, to_exten):
        return self._call_spy(channel, to_exten, 'B')

    def reset_stats(self, queue):
        return self.connection.reset_stats(queue)

    def hangup(self, channel):
        try:
            return self.connection.hangup(channel)
        except Exception as e:
            print(str(e))
            return {}

    def remove_from_queue(self, agent, queue):
        queue = realname_queue_rename(queue)
        self.connection = self._connect()
        try:
            return self.connection.remove_from_queue(agent, queue)
        except Exception as e:
            print(str(e))
            return {}
