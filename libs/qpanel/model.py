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
