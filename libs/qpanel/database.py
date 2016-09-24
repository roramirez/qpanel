# -*- coding: utf-8 -*-

#
# Class model Qpanel QueueLog Database
#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

from __future__ import absolute_import
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from .config import QPanelConfig


cfg = QPanelConfig()
engine = create_engine('%s://%s:%s@%s:%s/%s' %
                       (cfg.get('queue_log', 'adapter'),
                        cfg.get('queue_log', 'user'),
                        cfg.get('queue_log', 'password'),
                        cfg.get('queue_log', 'host'),
                        cfg.get('queue_log', 'port'),
                        cfg.get('queue_log', 'database')),
                       echo=cfg.is_debug, pool_recycle=3600)

# session
session_db = scoped_session(sessionmaker(bind=engine,
                                         autoflush=False,
                                         autocommit=False))

DeclarativeBase = declarative_base()
metadata = MetaData()
