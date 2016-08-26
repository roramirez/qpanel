# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#
import os
from sqlalchemy import Column, String, Integer, DateTime, create_engine, event
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import hashlib
import settings
import utils

PATH_DB = os.path.join(settings.ROOT_PATH, 'data', 'database.db')
engine = create_engine('sqlite:///' + PATH_DB, echo=False, pool_recycle=3600)

# session
session_dbconfig = scoped_session(sessionmaker(bind=engine,
                                               autoflush=False,
                                               autocommit=False))

DeclarativeBase = declarative_base()


class OperationCrud():
    def save(self):
        """
        add object into session and commit to database
        """
        session_dbconfig.add(self)
        return session_dbconfig.commit()

    def update(self):
        return session_dbconfig.commit()

    def delete(self):
        session_dbconfig.delete(self)
        return session_dbconfig.commit()


class Base(object, OperationCrud):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=utils.get_now())
    updated_at = Column(DateTime, onupdate=utils.get_now())

    def as_dict(self):
        return dict((col, getattr(self, col)) for col in
                    self.__table__.columns.keys())


class Config(DeclarativeBase, Base):

    __tablename__ = "config"

    namespace = Column(String)
    setting = Column(String)
    value = Column(String)

    query = session_dbconfig.query_property()

    def __init__(self, namespace, setting, value):
        self.namespace = namespace
        self.setting = setting
        self.value = value

    @staticmethod
    def add_data(*args, **kw):
        parse_config_to_db()


class User(DeclarativeBase):

    __tablename__ = "user"

    username = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    query = session_dbconfig.query_property()

    def __init__(self, username, password):
        m = hashlib.md5()
        m.update(password)
        self.username = username
        self.password = m.hexdigest()

    def as_dict(self):
        return {'name': self.name, 'username': self.username,
                'email': self.email}

    @staticmethod
    def count():
        return session_dbconfig.query(func.count(User.username)).scalar()

    @staticmethod
    def get_by_username(username):
        return session_dbconfig.query(User).\
                filter(User.username == username).first()

    @staticmethod
    def valid_user(username, password):
        user = User.get_by_username(username)
        if not user:
            return False
        if user.password == utils.to_md5(password):
            return True
        return False

    @staticmethod
    def add_data(*args, **kw):
        parse_user_into_db()


def parse_config_to_db():
    """
        Parser config file and add into config database
    """
    try:
        config_file = utils.open_config_ini_file(settings.PATH_FILE_CONFIG)
    except:
        config_file = utils.open_config_ini_file(
            os.path.join(settings.ROOT_PATH, 'samples', 'config.ini-dist'))

    sections = config_file.sections()
    for s in sections:
        items = dict(config_file.items(s))
        for i in items:
            value = config_file.get(s, i)
            if s == 'users':
                continue  # User is into other handler function
            else:
                new_cfg = Config(s, i, value)
                commit_object_db(new_cfg)


def parse_user_into_db():
    """
        Add users into db
    """
    items = get_value_sections('users')
    for i in items:
        u = User(i[0], i[1])
        commit_object_db(u)


def commit_object_db(obj):
    """
        add object into session and commit to database
    """
    session_dbconfig.add(obj)
    session_dbconfig.commit()


def get_value_sections(section):
    """
        get section from config file
    """
    try:
        config_file = utils.open_config_ini_file(settings.PATH_FILE_CONFIG)
        return config_file.items(section)
    except:
        return []


def get_settings(section=None):
    result = {}
    for setting in Config.query.all():
        if setting.namespace not in result.keys():
            result[setting.namespace] = {}
        result[setting.namespace][setting.setting] = setting.value
    if section is not None:
        tmp = {}
        if section in result.keys():
            tmp = result[section]
        result = tmp
    return result


def parser_config_from_dict(data):
    # convert values like
    # ... reset_stats[{'name': 'queue', 'values': 'now'},
    #                 {'name': 'queue2', 'values': 'now'}]
    # to
    # ... reset_stats{'queue': 'now', 'queue2': 'now'}
    # FIXME: Other way more smart please
    tmp = {}
    for key, value in data.items():
        tmp[key] = {}
        if type(value) is list:
            for l in value:
                if set(['name', 'value']).issubset(l.keys()):
                    tmp[key][l['name']] = l['value']
            continue
        for k, v in value.items():
            tmp[key][k] = v
    return tmp


def response_parser_config_from_schema(data, schema):
    for section in data:
        typo = schema['properties'][section]['type']
        if typo == 'array':
            tmp = []
            for v, k in data[section].items():
                tmp.append({'name': v, 'value': k})
            data[section] = tmp

    return data


def config_for_response(section=None):
    schema = settings.schema_settings
    data = get_settings(section)
    data = response_parser_config_from_schema(data, schema)
    return utils.casting_from_schema(data, schema)


def update_config_from_dict(data):
    data = parser_config_from_dict(data)
    for section in data:
        for cfg in data[section]:
            value = data[section][cfg]

            c = Config.query.filter(Config.namespace == section,
                                    Config.setting == cfg)
            if c.count() == 0:
                print("no exists into config", cfg, section)
                new_config = Config(section, cfg, value)
                new_config.save()
            else:
                c.update({'value': value})
                session_dbconfig.commit()


event.listen(User.__table__, "after_create", User.add_data)
event.listen(Config.__table__, "after_create", Config.add_data)
DeclarativeBase.metadata.create_all(engine)
