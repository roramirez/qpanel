import os
import sys
import ConfigParser

# import sqlalchemy from lib
dirname, filename = os.path.split(os.path.abspath(__file__))
sys.path.append(os.path.join(dirname, os.pardir, 'sqlalchemy', 'lib'))

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from config import QPanelConfig


cfg = QPanelConfig()
engine = create_engine ('%s://%s:%s@%s:%s/%s'  %
                         (cfg.get('queue_log', 'adapter'),
                          cfg.get('queue_log', 'user'),
                          cfg.get('queue_log', 'password'),
                          cfg.get('queue_log', 'host'),
                          cfg.get('queue_log', 'port'),
                          cfg.get('queue_log', 'database')
                         ),
                        echo=False)

# session
session_db = scoped_session(sessionmaker(bind=engine,
                                         autoflush=False,
                                         autocommit=False))

DeclarativeBase = declarative_base()
metadata = MetaData()
#Base.query = db_session.query_property()
