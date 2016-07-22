# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, String, Integer, TIMESTAMP, DateTime, Text,\
        Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import datetime

HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DB = os.path.join(HERE, os.pardir, os.pardir, 'data', 'database.db')
engine = create_engine('sqlite:///' + PATH_DB, echo=True)

# session
session_db = scoped_session(sessionmaker(bind=engine,
                                         autoflush=False,
                                         autocommit=False))

DeclarativeBase = declarative_base()
metadata = MetaData()


def _get_now():
    return datetime.datetime.now()


class ColumnList(DeclarativeBase):
    __tablename__ = "column_list"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    key = Column(Boolean, default=False)
    list_id = Column(Integer, ForeignKey('list.id'), nullable=False)
    created_at = Column(DateTime, default=_get_now())
    created_at = Column(DateTime, onupdate=_get_now())

    def __repr__(self):
        return "<ColumnList(id='%s', name='%s', type='%s')>" % (
            self.id, self.name, self.type)


class List(DeclarativeBase):
    __tablename__ = "list"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, default=_get_now())
    created_at = Column(DateTime, onupdate=_get_now())

    def __repr__(self):
        return "<List(id='%s', name='%s')>" % (self.id, self.name)



class Contact(DeclarativeBase):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
    number = Column(String)
    data = Column(Text)
    list_id = Column(Integer, ForeignKey('list.id'), nullable=False)
    created_at = Column(DateTime, default=_get_now())
    created_at = Column(DateTime, onupdate=_get_now())

    def __repr__(self):
        return "<Contact(id='%s', number='%s', data='%s')>" % (
            self.id, self.number, self.data)


class Campaign(DeclarativeBase):
    __tablename__ = "campaign"

    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    name = Column(String)
    text = Column(String)
    init = Column(TIMESTAMP)
    end = Column(TIMESTAMP)
    list_id = Column(Integer, ForeignKey('list.id'), nullable=True)
    created_at = Column(DateTime, default=_get_now())
    created_at = Column(DateTime, onupdate=_get_now())

    def __init__(self, name, init, end):
        self.name = name
        self.init = init
        self.end = end

    def __repr__(self):
        return "<Campaign(id='%s', name='%s', init='%s', end='%s')>" % (
            self.id, self.name, self.init, self.end)


def _commit_object_db(obj):
    """
        add object into session and commit to database
    """
    session_db.add(obj)
    session_db.commit()

DeclarativeBase.metadata.create_all(engine)
