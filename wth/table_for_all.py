import requests
import fake_useragent
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time
import socks
import socket
import logging
from aiogram import types
import os



logging.basicConfig(level=logging.INFO)

engine = create_engine('sqlite:///mydatabase.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class UserData(Base):
    __tablename__ = 'dauns'

    id = Column(Integer, primary_key=True)
    login_in_site_start = Column(String)
    passwd_on_site_start = Column(String)
    user_id = Column(Integer)


class UserDating(Base):
    __tablename__ = 'user_dating'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name_on_site = Column(String)
    which_group_on_site = Column(String)
    how_many_comment = Column(String)
    when_reg = Column(String)
    here_was = Column(String)

Base.metadata.create_all(engine)

