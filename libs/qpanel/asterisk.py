# -*- coding: utf-8 -*-

#
# Class Qpanel for Asterisk
#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

from __future__ import absolute_import
from Asterisk.Manager import *


class ConnectionErrorAMI(Exception):
    '''
    This exception is raised when is not possible or is not connected to
    AMI for a requested action.
    '''
    _error = 'Not Connected'
    pass


class AsteriskAMI:

    def __init__(self, host, port, user, password):
        '''
        Initialise a class for Asterisk
        '''
        self.host = host
        self.port = int(port)
        self.password = password
        self.user = user
        self.is_connected = False
        self.connection = self.connect_ami()

    def connect_ami(self):
        try:
            manager = Manager((self.host, self.port), self.user, self.password)
            return manager
        except:
            return None

    def queueStatus(self):
        return self.getQueues()

    def getQueues(self):
        if self.connection is None:
            raise ConnectionErrorAMI(
                "Failed to connect to server at '{}:{}' for user {}\n"
                'Please check that Asterisk running and accepting AMI '
                'connections.'.format(self.host, self.port, self.user))

        cmd = self.connection.QueueStatus()
        return cmd

    def spy(self, channel, where_listen, option=None):
        '''Generate a Originate event by Manager to used Spy Application

        Parameters
        ----------
        channel: str
            channel to create Originate action tu use ChanSpy
        where_listen: str
            channel where listen the spy action.
        option: str
            other option to add for execute distinct options.
                whisper: w
                barge: B
            other string to add ChanSpy Command
            The option is concatenate to ',q'

        Returns
        -------
        originate result command : Dictionary
            if case the fail return return  {'Response': 'failed',
                                             'Message': str(msg)}
        '''

        options = ',q'
        if option:
            options = options + option
        try:
            # create a originate call for Spy a exten
            return self.connection.Originate(where_listen,
                                             application='ChanSpy',
                                             data=channel + options,
                                             async='yes')
        except Asterisk.Manager.ActionFailed as msg:
            return {'Response': 'failed', 'Message': str(msg)}
        except PermissionDenied as msg:
            return {'Response': 'failed', 'Message': 'Permission Denied'}

    def hangup(self, channel):
        '''Hangup Channel

        Parameters
        ----------
        channel: str
            channel to hangup
        Returns
        -------
        hangup result action : Dictionary
            if case the fail return return  {'Response': 'failed',
                                             'Message': str(msg)}
        '''
        try:
            # hangup channels
            return self.connection.Hangup(channel)
        except Asterisk.Manager.ActionFailed as msg:
            return {'Response': 'failed', 'Message': str(msg)}
        except PermissionDenied as msg:
            return {'Response': 'failed', 'Message': 'Permission Denied'}

    def reset_stats(self, queue):
        'Reset stats for <queue>.'
        id = self.connection._write_action('QueueReset', {'Queue': queue})
        return self.connection._translate_response(
            self.connection.read_response(id))

    def isConnected(self):
        if not self.connection:
            return False
        return True

    def remove_from_queue(self, agent, queue):
        '''Remove a <agent> from a <queue>

        Parameters
        ----------
        agent: str
            Agent or Inteface to remove
        queue: str
            name of queue from remove agent
        Returns
        -------
        originate result command : Dictionary
            if case the fail return return  {'Response': 'failed',
                                             'Message': str(msg)}
        '''
        try:
            return self.connection.QueueRemove(queue, agent)
        except Asterisk.Manager.ActionFailed as msg:
            return {'Response': 'failed', 'Message': str(msg)}
        except PermissionDenied as msg:
            return {'Response': 'failed', 'Message': 'Permission Denied'}
