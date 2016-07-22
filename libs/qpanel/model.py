# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016 Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#
import os
from sqlalchemy import Column, String, Integer, TIMESTAMP, DateTime, Text,\
        Boolean, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base
import utils

HERE = os.path.abspath(os.path.dirname(__file__))
PATH_DB = os.path.join(HERE, os.pardir, os.pardir, 'data', 'database.db')
engine = create_engine('sqlite:///' + PATH_DB, echo=True)

# session
session_db = scoped_session(sessionmaker(bind=engine,
                                         autoflush=False,
                                         autocommit=False))


class Base(object):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=utils.get_now())
    updated_at = Column(DateTime, onupdate=utils.get_now())

    def save(self):
        _commit_object_db(self)

    def as_dict(self):
        return dict((col, getattr(self, col)) for col in
                    self.__table__.columns.keys())


DeclarativeBase = declarative_base(cls=Base)


class ColumnList(DeclarativeBase):
    __tablename__ = "column_list"

    name = Column(String)
    type = Column(String)
    key = Column(Boolean, default=False)
    list_id = Column(Integer, ForeignKey('list.id'), nullable=False)

    def __repr__(self):
        return "<ColumnList(id='%s', name='%s', type='%s')>" % (
            self.id, self.name, self.type)


class List(DeclarativeBase):
    __tablename__ = "list"

    name = Column(String)
    contacts = relationship("Contact", order_by="Contact.id", backref="list")
    campaigns = relationship("Campaign", back_populates="list")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<List(id='%s', name='%s')>" % (self.id, self.name)


class Contact(DeclarativeBase):
    __tablename__ = "contact"

    number = Column(String)
    data = Column(Text)
    list_id = Column(Integer, ForeignKey('list.id'), nullable=False)

    def __repr__(self):
        return "<Contact(id='%s', number='%s', data='%s')>" % (
            self.id, self.number, self.data)


class Campaign(DeclarativeBase):
    __tablename__ = "campaign"

    status = Column(Integer)
    name = Column(String)
    text = Column(String)
    init = Column(TIMESTAMP)
    end = Column(TIMESTAMP)
    list_id = Column(Integer, ForeignKey('list.id'), nullable=True)
    list = relationship("List", back_populates="campaigns")

    def __init__(self, name, init, end):
        self.name = name
        self.init = init
        self.end = end

    def __repr__(self):
        return "<Campaign(id='%s', name='%s', init='%s', end='%s')>" % (
            self.id, self.name, self.init, self.end)


class TmpContactList(DeclarativeBase):
    __tablename__ = "tmp_contact_list"

    key = Column(String)
    content = Column(Text)
    list_id = Column(Integer, ForeignKey('list.id'), nullable=True)


def _commit_object_db(obj):
    """
        add object into session and commit to database
    """
    session_db.add(obj)
    session_db.commit()

DeclarativeBase.metadata.create_all(engine)
