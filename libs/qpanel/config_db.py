# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#
import os
from sqlalchemy import create_engine, MetaData, event
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from config import QPanelConfig


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

    @staticmethod
    def add_data(*args, **kw):
        parse_config_to_db()


def parse_config_to_db():
    """
        Parser config file and add into config database
    """
    config_file = QPanelConfig().config
    sections = config_file.sections()
    for s in sections:
        items = dict(config_file.items(s))
        for i in items:
            value = config_file.get(s, i)
            new_cfg = Config(s, i, value)
            session_dbconfig.add(new_cfg)
            session_dbconfig.commit()


event.listen(Config.__table__, "after_create", Config.add_data)
DeclarativeBase.metadata.create_all(engine)
