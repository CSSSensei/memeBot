from aiogram.filters import Command
import os
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from config_data.config import bot
from filters import filters, format_text
from DB.users_info import UserDB, UserQueryDB
from keyboards import admin_keyboards
from callbacks.callback_info import *
import datetime

router = Router()

router.message.filter(filters.AdminUser())


@router.message(Command(commands='get_users'))  # /get_users
async def users_command(message: Message):
    await admin_keyboards.get_users_by_page(message.from_user.id)


@router.message(Command(commands='user_query'))  # /user_query
async def user_query_command(message: Message):
    user_id_to_find = format_text.find_first_number(message.text)
    await admin_keyboards.user_query_by_page(message.from_user.id, user_id_to_find)


@router.message(Command(commands='getcoms'))  # /getcoms
async def all_commands(message: Message):
    await message.answer('/help\n'
                         '/get_users\n'
                         '/query <i>(int)</i> — последние <i>n</i> среди всех запросов\n'
                         '/user_query <i>(user_id)</i> — запросы пользователя <i>(user_id)</i>')


@router.message(Command(commands='delete_pictures'))
async def delete_pictures_in_directory(message: Message):
    try:
        directory = os.path.join(os.path.dirname(__file__), os.pardir, 'pictures')
        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            os.remove(file_path)
        await message.answer('Файлы удалены! ✅')
    except Exception as e:
        await bot.send_message(chat_id=972753303, text=f'Произошла ошибка! Код 634\n{e}')


@router.message(Command(commands='query'))  # /query
async def query_command(message: Message):
    txt = ''
    amount = format_text.find_first_number(message.text)
    if not amount:
        amount = 5
    for user in await UserQueryDB.get_last_queries(amount):
        username = await UserDB.get_username(user.user_id)
        line = (f'<i>@{username if username else user.user_id}</i> — '
                f'{", ".join(f"[{datetime.datetime.utcfromtimestamp(unix_time) + datetime.timedelta(hours=3)}]: <blockquote>{format_text.format_string(query)}</blockquote>" for unix_time, query in user.queries.items())}\n\n')
        if len(line) + len(txt) < 4096:
            txt += line
        else:
            try:
                await message.answer(text=txt)
            except Exception as e:
                await message.answer(text=f'Произошла ошибка!\n{e}')
            txt = line
    if len(txt) != 0:
        await message.answer(txt)
    else:
        await message.answer('Запросов не было')


@router.callback_query(CutMessageCallBack.filter())
async def cut_message_distributor(callback: CallbackQuery, callback_data: CutMessageCallBack):
    action = callback_data.action
    page = callback_data.page
    user_id = callback_data.user_id
    if action == 1:
        await admin_keyboards.get_users_by_page(callback.from_user.id, page, callback.message.message_id)
    elif action == 2:
        await admin_keyboards.user_query_by_page(callback.from_user.id, user_id, page, callback.message.message_id)
    elif action == -1:
        await callback.answer()
