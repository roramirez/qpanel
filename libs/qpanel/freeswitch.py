# -*- coding: utf-8 -*-

#
# Class Qpanel for Freeswitch
#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#


import ESL
import utils

# Default
defaultESLport = 8021
defaultESLpassword = 'ClueCon'


class NotConnected(BaseException):
    '''
    This exception is raised when is not possible or is not connected
    to ELS for a requested action.
    '''
    _error = 'Not Connected'


class Freeswitch:

    def __init__(self, host='127.0.0.1', port=defaultESLport,
                 password=defaultESLpassword):
        '''
        Initialise a class for Freeswitch
        '''
        self.host = host or '127.0.0.1'
        self.port = int(port or defaultESLport)
        self.password = password or defaultESLpassword
        self.connection = ESL.ESLconnection(self.host,
                                            self.port,
                                            self.password)

    def getQueues(self):
        cmd = self.command('callcenter_config queue list')
        cmd = self._parserBodyCommand(cmd)
        return cmd

    def getAgents(self, queue_name):
        cmd = self.command('callcenter_config queue list agents %s' %
                           queue_name)
        cmd = self._parserBodyCommand(cmd)
        return cmd

    def getCalls(self, queue_name):
        output = {}
        cmd = self.command('show channels')
        cmd = self._parserBodyCommand(cmd, ',')
        for channel in cmd:
            if cmd[channel]['Application'] == 'callcenter':
                if cmd[channel]['ApplicationData'] == queue_name:
                    output[channel] = cmd[channel]

        return output

    def queueStatus(self):
        queues = self.getQueues()
        for queue in queues:
            queues[queue]['members'] = self.getAgents(queue)
            queues[queue]['entries'] = self.getCalls(queue)
            queues[queue]['Calls'] = len(queues[queue]['entries'])
        return queues

    def command(self, command):
        if not self.isConnected():
            raise NotConnected

        e = self.connection.api(command)
        if e:
            return e.getBody()

    def _parserBodyCommand(self, body, delimiter='|'):
        output = {}

        if body:
            tmp = body.splitlines()
        if len(tmp) > 0:
            header = tmp[0].split(delimiter)

        for l in tmp[1:-1]:
            line = l.split(delimiter)
            if len(line) < len(header):
                continue
            i = 0
            tmp_dict = {}
            for e in line:
                tmp_dict[utils.underscore_to_camelcase(header[i])] = e
                i = i + 1
            output[line[0]] = tmp_dict

        return output

    def isConnected(self):
        return self.connection.connected()
