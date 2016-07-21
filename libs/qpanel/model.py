# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, String, Integer, TIMESTAMP, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import datetime

HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DB = os.path.join(HERE, os.pardir, os.pardir, 'data', 'database.db')
engine = create_engine('sqlite:///' + PATH_DB, echo=True)

# session
session_db = scoped_session(sessionmaker(bind=engine,
                                         autoflush=False,
                                         autocommit=True))

DeclarativeBase = declarative_base()
metadata = MetaData()


def _get_now():
    return datetime.datetime.now()


class Campaign(DeclarativeBase):
    __tablename__ = "campaign"

    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    name = Column(String)
    text = Column(String)
    init = Column(TIMESTAMP)
    end = Column(TIMESTAMP)
    created_at = Column(DateTime, default=_get_now())
    created_at = Column(DateTime, onupdate=_get_now())

    def __init__(self, name, init, end):
        self.name = name
        self.init = init
        self.end = end


def _commit_object_db(obj):
    """
        add object into session and commit to database
    """
    session_db.add(obj)
    session_db.commit()

DeclarativeBase.metadata.create_all(engine)
