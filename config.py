import asyncio
import calendar
import datetime
import io
import json
import os
import time
import shutil
import aiohttp
import aiofiles

import aiogram.utils.chat_action

import requests
import random
from typing import List, Dict, Union
from pathlib import Path

import tzlocal
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter, BaseFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile, InputMediaPhoto, InputMediaDocument, InputMediaVideo
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ContentType,
                           MessageReactionUpdated)
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types.reaction_type_emoji import ReactionTypeEmoji
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv, find_dotenv
from aiogram.client.session.aiohttp import AiohttpSession
from mem_generator import create_meme
from users_info import *
import g4f

SETTINGS_ACTION = -1
USERMODE_ACTION = 0
UPPERTEXT_ACTION = 1
BOTTOMTEXT_ACTION = 2
UPPERSTROKE_ACTION = 3
BOTTOMSTROKE_ACTION = 4
TEXTCASE_ACTION = 5
SETsmallcase = 6
SETgiantcase = 7

load_dotenv(find_dotenv())

API_TOKEN: str = os.getenv('TOKEN')
storage: MemoryStorage = MemoryStorage()

bot: Bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp: Dispatcher = Dispatcher(storage=storage)
gpt_client = g4f.client.Client()

current_dm_id = {}
states_users = {}
caption_global = {}
hz_answers = ['Я тебя не понимаю...', 'Я не понимаю, о чем ты', 'Что ты имеешь в виду? 🧐', 'Я в замешательстве 🤨',
              'Не улавливаю смысла 🙃', 'Что ты пытаешься сказать❓', 'Не понимаю твоего сообщения 😕',
              '🤷‍♂️ Не понимаю 🤷‍♀️']
emoji_lol = ['🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🫐', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🍆', '🥑', '🫛', '🥦', '🥬', '🥒', '🌶', '🫑',
             '🌽', '🥕', '🫒', '🧄', '🧅', '🥔', '🍠', '🫚', '🥐', '🥯', '🍞', '🥖', '🥨', '🧀', '🥚', '🍳', '🧈', '🥞', '🧇', '🌭', '🍔', '🍟', '🍕', '🥪', '🥙', '🧆',
             '🌮', '🌯', '🫔', '🥗', '🥘', '🫕', '🥫', '🍝', '🍜', '🍲', '🍛', '🍣', '🍱', '🥟', '🦪', '🍤', '🍙', '🍚', '🍘', '🍥', '🥠', '🥮', '🍡', '🍧', '🍨', '🍦',
             '🥧', '🧁', '🍰', '🎂', '🍮', '🍭', '🍬', '🍫', '🍿', '🍩', '🍪', '🌰', '🍯', '🥛', '🫗', '🍼', '🫖', '☕️', '🍵', '🧃', '🥤', '🧋', '🍶', '🍾', '🧊', '⚽️',
             '🏀', '🏈', '⚾️', '🥎', '🎾', '🏐', '🏉', '🥏', '🎱', '🪀', '🏓', '🏸', '🎧', '🎫', '🎟', '🎲', '♟', '🎯', '🎳', '🎮', '🎰', '🧩', '🗾', '🎑', '🏞', '🌅',
             '🌄', '🌠', '🎇', '🎆', '🌇', '🌆', '🏙', '🌃', '🌌', '🌉', '🌁', '💣', '🧨', '💊', '🎁', '🎈', '🛍', '🪩', '📖', '📚', '📙', '📘', '📗', '📕', '📒', '📔',
             '📓', '📰', '🗞', '🧵', '👚', '👕', '👖', '👔', '💼', '👜', '🎩', '🧢', '👒', '🎓', '🧳', '👓', '🕶', '🥽', '🌂', '💍', '🐶', '🐭', '🐹', '🐰', '🦊', '🐻',
             '🐼', '🐻‍❄️', '🐨', '🐯', '🦁', '🐸', '🐵', '🙈', '🙉', '🙊', '🐒', '🐱', '🐔', '🐧', '🐦', '🐤', '🐣', '🐥', '🪿', '🦆', '🐦‍⬛️', '🦅', '🦉', '🦇', '🐺',
             '🐴', '🦄', '🐝', '🦋', '🦖', '🦕', '🐙', '🦑', '🪼', '🦐', '🐬', '🐋', '🐳', '🦈', '🦭', '🪽', '🕊', '🪶', '🐉', '🐲', '🦔', '🐁', '🌵', '🎄', '🌲', '🌳',
             '🌴', '🪵', '🌱', '🌿', '☘️', '🍀', '🎍', '🪴', '🎋', '🍃', '🍂', '🍁', '🪺', '🐚', '🪸', '🪨', '🌾', '💐', '🌷', '🌹', '🥀', '🪻', '🪷', '🌺', '🌸', '🌼',
             '🌻', '🌎', '🌍', '🌏', '🪐', '💫', '⭐️', '✨', '💥', '🔥', '🌪', '🌈', '☀️', '🌤', '⛅️', '🌥', '☁️', '☃️', '⛄️', '💨', '☂️', '🌊', '🌫']
emoji_banned = '⛔❗🤯😳❌⭕🛑📛🚫💢🚷📵🔴🟥💣🗿🐓🙊🙉🙈🐷🫵🥲🙁😕😟😔😞😧😦😯🙄😵💀🚨😐'
dice_points = {'🎲': 6, '🎯': 6, '🎳': 6, '🏀': 4, '⚽': 3, '🎰': 64}
# replicas = {}
# with open('DB/replicas.txt', 'r', encoding='utf-8') as file:
#     replicas = json.load(file)
#     
modes_name = {
    'in': ['Мемас', 100],
    'de': ['Демотиватор', 101],
    'bo': ['Чтиво', 102]
}
MODE_CODES_set = {mode[1] for mode in modes_name.values()}

COLORS = {
    'Нигер': ['#000000', 38],
    'Пурпурная пицца': ['#FF00FF', 39],
    'Баклажанный': ['#800080', 41],
    'Месячные': ['#FF0000', 42],
    'Детская неожиданность': ['#800000', 43],
    'Пись-пись': ['#FFFF00', 44],
    'Рвота': ['#808000', 45],
    'Вердепомовый': ['#00FF00', 46],
    'Индийский': ['#008000', 47],
    'Яйца странствующего дрозда': ['#00FFFF', 48],
    'Окраска птицы чюрок': ['#008080', 49],
    'Цвет уверенности': ['#0000FF', 51],
    'Форма морских офицеров': ['#000080', 52],
    'Белоснежка': ['#FFFFFF', 53],
}
COLOR_CODES_set = {color[1] * (10 ** power) for color in COLORS.values() for power in range(4)}


async def get_neuro_comment(message_text):
    response = gpt_client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user",
                   "content": f"Представь, что ты гопник. Объясни, что такое {message_text}, но говоря как некомпетентный человек и в дворовом стиле"}],
    )
    return response.choices[0].message.content


async def loading_indicator(chat_id, mes_id):
    clock = '🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛'
    cnt = 0
    while True:
        await bot.edit_message_text(chat_id=chat_id, message_id=mes_id,
                                    text=f'Секунду, братан, шестерёнки работают {clock[cnt % len(clock)]}')
        await asyncio.sleep(1)
        cnt += 1


class SetsCallBack(CallbackData, prefix="sets"):
    action: int


def get_keyboard(sets: UserDB):
    array_buttons: list[list[InlineKeyboardButton]] = [[], [], [], []]
    array_buttons[0].append(InlineKeyboardButton(text='Режим', callback_data=SetsCallBack(action=USERMODE_ACTION).pack()))
    array_buttons[1].append(InlineKeyboardButton(text='Цвет верхнего текста', callback_data=SetsCallBack(action=UPPERTEXT_ACTION).pack()))
    array_buttons[1].append(InlineKeyboardButton(text='Цвет нижнего текста', callback_data=SetsCallBack(action=BOTTOMTEXT_ACTION).pack()))
    array_buttons[2].append(InlineKeyboardButton(text='Контур верхнего текста', callback_data=SetsCallBack(action=UPPERSTROKE_ACTION).pack()))
    array_buttons[2].append(InlineKeyboardButton(text='Контур нижнего текста', callback_data=SetsCallBack(action=BOTTOMSTROKE_ACTION).pack()))
    array_buttons[3].append(InlineKeyboardButton(text='Регистр текста', callback_data=SetsCallBack(action=TEXTCASE_ACTION).pack()))

    markup = InlineKeyboardMarkup(inline_keyboard=array_buttons)
    return markup


def get_mode_keyboard(current_mode: str):
    array_buttons: list[list[InlineKeyboardButton]] = []
    cnt = 0
    button_in_row = 3
    for mode_code, mode_name in modes_name.items():
        if cnt % button_in_row == 0:
            array_buttons.append([])
        emoji = ' ✅' if mode_code == current_mode else ''
        array_buttons[cnt // button_in_row].append(
            InlineKeyboardButton(text=mode_name[0] + emoji, callback_data=SetsCallBack(action=mode_name[1]).pack()))
        cnt += 1
    array_buttons.append([InlineKeyboardButton(text='Назад', callback_data=SetsCallBack(action=SETTINGS_ACTION).pack())])
    markup = InlineKeyboardMarkup(inline_keyboard=array_buttons)
    return markup


def get_mode_name_by_code(number, dictionary=None):
    if dictionary is None:
        dictionary = modes_name
    for key, value in dictionary.items():
        if value[1] == number:
            return key
    return None


def get_color_keyboard(current_color, offset=1):
    array_buttons: list[list[InlineKeyboardButton]] = []
    cnt = 0
    button_in_row = 3
    for color_name, color_code in COLORS.items():
        if cnt % button_in_row == 0:
            array_buttons.append([])
        emoji = '✅ ' if color_code[0] == current_color else ''
        array_buttons[cnt // button_in_row].append(
            InlineKeyboardButton(text=emoji + color_name, callback_data=SetsCallBack(action=color_code[1] * offset).pack()))
        cnt += 1
    array_buttons.append([InlineKeyboardButton(text='Назад', callback_data=SetsCallBack(action=SETTINGS_ACTION).pack())])
    markup = InlineKeyboardMarkup(inline_keyboard=array_buttons)
    return markup


def get_colorhash_by_code(number, dictionary=None):
    if dictionary is None:
        dictionary = COLORS
    for key, value in dictionary.items():
        if value[1] == number:
            return value[0]
    return '#000000'


def get_colorname_by_hashcode(hash):
    for color_name, code_info in COLORS.items():
        if code_info[0] == hash:
            return color_name
    return hash

    # Пример использования
    input_color_code = '#800080'
    color_name = get_color_name(input_color_code, COLORS)
    print(color_name)  # Выведет 'Баклажанный'


def get_case_keyboard(giant: bool):
    array_buttons: list[list[InlineKeyboardButton]] = []
    if not giant:
        txt = 'УСТАНОВИТЬ БАЛЬШИЕ БУКАВЫ'
        action = SETgiantcase
    else:
        txt = 'поставить маленькие буковки'
        action = SETsmallcase
    array_buttons.append([InlineKeyboardButton(text=txt, callback_data=SetsCallBack(action=action).pack())])
    array_buttons.append([InlineKeyboardButton(text='Назад', callback_data=SetsCallBack(action=SETTINGS_ACTION).pack())])
    markup = InlineKeyboardMarkup(inline_keyboard=array_buttons)
    return markup


if __name__ == '__main__':
    pass
