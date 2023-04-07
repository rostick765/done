import socks
import socket
import requests
import fake_useragent
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time
import logging
from aiogram import types
import os
from table_for_all import *

# устанавливаем прокси-сервер и создаем объект сокета
socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket

# создаем объект движка базы данных
engine = create_engine('sqlite:///mydatabase.db', echo=True)

# создаем сессию базы данных
DBSession = sessionmaker(bind=engine)
req_session = requests.Session()

# устанавливаем user-agent
user_agent = fake_useragent.UserAgent().random
header = {'user-agent': user_agent}

link = "https://anime1.animebesst.org/"

# Получаем все записи из таблицы UserData
users = session.query(UserData).all()

# Итерируемся по всем пользователям и выводим их логины и пароли
for user in users:
    username = user.login_in_site_start
    password = user.passwd_on_site_start

    data = {
        'login_name': username,
        'login_password': password
    }

    # отправляем POST-запрос на сайт для авторизации пользователя
    req_session.post(link, data=data, headers=header)


    link_on_profile = f'https://anime1.animebesst.org/user/{username}/'
    print(link_on_profile)

    # отправляем GET-запрос на страницу профиля пользователя
    response = req_session.get(link_on_profile)

    soup = BeautifulSoup(response.text, 'html.parser')

    all_info = soup.find('ul', class_= 'ul-stat')
    full_name1 = all_info.find_all('li')[0].text
    full_name2 = all_info.find_all('li')[1].text
    full_name3 = all_info.find_all('li')[2].text
    full_name4 = all_info.find_all('li')[3].text
    full_name5 = all_info.find_all('li')[4].text

    # создаем сессию базы данных
    db_session = DBSession()

    # Ищем запись в базе данных
    user_in_db = db_session.query(UserDating).filter_by(name_on_site=full_name1).first()

    if user_in_db is None:
        # Если записи нет, добавляем ее
        user_in_sukaba = UserDating(name_on_site=full_name1, which_group_on_site=full_name2, how_many_comment=full_name3, when_reg=full_name4, here_was=full_name5)
        db_session.add(user_in_sukaba)
        db_session.commit()

    else:
        # Если запись уже существует, обновляем ее значения
        user_in_db.name_on_site = full_name1
        user_in_db.which_group_on_site = full_name2
        user_in_db.how_many_comment = full_name3
        user_in_db.when_reg = full_name4
        user_in_db.here_was = full_name5
        db_session.commit()


    db_session.close()
