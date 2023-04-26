from sqlalchemy import Column, Integer, String, Sequence, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import connector

class Account(connector.Manager.Base):
    __tablename__ = 'accounts'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    position = Column(String(50))
    name = Column(String(50))
    password = Column(String(12))


class Event(connector.Manager.Base):
    __tablename__ = 'events'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    type = Column(String(50))
    time = Column(String(100))