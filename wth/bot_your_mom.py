from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from confagig import TOKEN
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import FSMContext
import asyncio
import logging
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.types import CallbackQuery
import confagig
import os
from aiogram.types import InputFile
import aiogram.utils.markdown as md
from aiogram.types import ParseMode
from aiogram.utils import exceptions
from aiogram.utils.markdown import text
from aiogram.types import ContentType
import aiogram
import subprocess
from table_for_all import*
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from table_for_all import UserDating

logging.basicConfig(level=logging.INFO)


bot = Bot(token=TOKEN)

dp = Dispatcher(bot)


async def run_sukabaka():
    subprocess.run(['python', 'how_already_zaebal.py'])

@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    await message.answer(text="Для начала отправьте txt файл с логином и паролем.")


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def handle_text_document(message: types.Message, state: FSMContext):
    await message.answer('Обработка....')
    """
    Обработчик файла .txt. Сохраняет файл, читает его содержимое и сохраняет логин и пароль в базу данных.
    """
    session = Session()




    # Проверяем, что файл .txt
    if message.document.mime_type == "text/plain":

        # Получаем информацию о файле
        file_info = await bot.get_file(message.document.file_id)
        file_path = file_info.file_path

        # Скачиваем файл
        file_name = message.document.file_name
        await bot.download_file(file_path, f'./{file_name}')

        # Читаем содержимое файла
        with open(file_name, 'r') as file:
            file_lines = file.readlines()

        # Извлекаем логин и пароль из каждой строки файла
        for line in file_lines:
            login, passwd = line.strip().split(':')

            # Проверяем, есть ли в базе данных объект с такими параметрами
            user_data = session.query(UserData).filter_by(login_in_site_start=login, passwd_on_site_start=passwd).all()

            if not user_data:
                # Если объекта нет, то создаем его и добавляем в базу данных
                user_data = UserData(login_in_site_start=login, passwd_on_site_start=passwd)
                session.add(user_data)
                session.commit()
        session.close()
        await run_sukabaka()
        await message.answer('Получить результат --> /get_userdating')

@dp.message_handler(commands=['get_userdating'])
async def get_userdating_handler(message: types.Message):
    # получаем все записи из таблицы UserDating
    users = session.query(UserDating).all()

    # формируем сообщение с данными из таблицы
    response = ''
    for user in users:
        response += f'{user.name_on_site}\n'
        response += f'{user.which_group_on_site}\n'
        response += f'{user.how_many_comment}\n'
        response += f'{user.when_reg}\n'
        response += f'{user.here_was}\n\n'

    # отправляем сообщение с данными пользователю
    await message.answer(response)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
