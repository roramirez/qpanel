import os
import sys
import ConfigParser

#import sqlalchemy from libs
dirname, filename = os.path.split(os.path.abspath(__file__))
sys.path.append(os.path.join(dirname, os.pardir, 'sqlalchemy', 'lib'))

from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import mapper
from database import session_db, metadata, DeclarativeBase

# Class queue_log Table
queue_log = Table(u'queue_log', metadata,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('time', Text),
    Column('callid', Text),
    Column('queuename', Text),
    Column('agent', Text),
    Column('event', Text),
    Column('data', Text),
    Column('data1', Text),
    Column('data2', Text),
    Column('data3', Text),
    Column('data4', Text),
    Column('data5', Text),
)

class QueueLog(DeclarativeBase):
    __table__ = queue_log
    query = session_db.query_property()
    #relation definitions
    def as_dict(self):
        return {'id': self.id,
                'time': self.time.split('.')[0],
                'callid': self.callid,
                'queuename': self.queuename,
                'agent': self.agent,
                'event': self.event,
                'data': self.data,
                'data1': self.data1,
                'data2': self.data2,
                'data3': self.data3,
                'data4': self.data4,
                'data5': self.data5
               }


def queuelog_event_by_range_and_types(start_date, end_date, events=None,
                                      agent=None, queue=None):
    try:
        q = session_db.query(QueueLog)
        if from:
            q = q.filter(QueueLog.time >= from)
        if to:
            q = q.filter(QueueLog.time <= to)
        if events:
            q = q.filter(QueueLog.event.in_(events))
        if agent:
            q = q.filter(QueueLog.agent.in_(agent))
        if queue:
            q = q.filter(QueueLog.queuename == queue)
        return q.order_by(QueueLog.id.asc()).all()
    except NoResultFound, e:
        return None

def queuelog_count_answered(start_date, end_date, agent=None, queue=None):
    events = ['CONNECT']
    data =  queuelog_event_by_range_and_types(start_date, end_date, events,
                                              agent, queue)
    return len(data)

def queuelog_count_inbound(start_date, end_date, agent=None, queue=None):
    events = ['ENTERQUEUE']
    calls = []
    data =  queuelog_event_by_range_and_types(start_date, end_date, events,
                                              agent, queue)

    for call in data:
        if call.callid not in calls:
            calls.append(call.callid)
    return len(calls)

def queuelog_count_abandon(start_date, end_date, agent=None, queue=None):
    events = ['ABANDON']
    data =  queuelog_event_by_range_and_types(start_date, end_date, events,
                                              agent, queue)
    return len(data)

def queuelog_seconds_wait_abandon(start_date, end_date, agent=None, queue=None):
    events = ['ABANDON']
    seconds = 0
    data =  queuelog_event_by_range_and_types(start_date, end_date, events,
                                              agent, queue)
    for call in data:
        seconds = seconds + int(call.data3)
    return seconds

def queuelog_seconds_wait(start_date, end_date, agent=None, queue=None):
    events = ['CONNECT']
    seconds = 0
    data =  queuelog_event_by_range_and_types(start_date, end_date, events,
                                              agent, queue)
    for call in data:
        seconds = seconds + int(call.data1)
    return seconds

def queuelog_seconds_talking(start_date, end_date, agent=None, queue=None):
    events = ['COMPLETECALLER', 'COMPLETEAGENT']
    seconds = 0
    data =  queuelog_event_by_range_and_types(start_date, end_date, events,
                                              agent, queue)
    for call in data:
        seconds = seconds + int(call.data2)
    return seconds
