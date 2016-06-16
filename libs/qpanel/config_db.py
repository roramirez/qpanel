# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#
import os
import datetime
import sys
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound


HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DB = os.path.join(HERE, os.pardir, os.pardir, 'data', 'database.db')
engine = create_engine('sqlite:///' + PATH_DB, echo=True)

# session
session_dbconfig = scoped_session(sessionmaker(bind=engine,
                                               autoflush=False,
                                               autocommit=False))

DeclarativeBase = declarative_base()
metadata = MetaData()


class Config(DeclarativeBase):

    __tablename__ = "config"

    id = Column(Integer, primary_key=True)
    namespace = Column(String)
    setting = Column(String)
    value = Column(String)

    def __init__(self, namespace, setting, value):
        self.namespace = namespace
        self.setting = setting
        self.value = value

DeclarativeBase.metadata.create_all(engine)