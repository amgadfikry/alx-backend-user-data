#!/usr/bin/env python3
""" module for user model """
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """ user model table by sqlalchemy """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id =  Column(String, nullable=False)
    reset_token = Column(String, nullable=False)
