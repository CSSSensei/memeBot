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
    array_buttons[0].append(InlineKeyboardButton(text='Режим', callback_data=SetsCallBack(action=0).pack()))
    array_buttons[1].append(InlineKeyboardButton(text='Цвет верхнего текста', callback_data=SetsCallBack(action=1).pack()))
    array_buttons[1].append(InlineKeyboardButton(text='Цвет нижнего текста', callback_data=SetsCallBack(action=2).pack()))
    array_buttons[2].append(InlineKeyboardButton(text='Контур верхнего текста', callback_data=SetsCallBack(action=3).pack()))
    array_buttons[2].append(InlineKeyboardButton(text='Контур нижнего текста', callback_data=SetsCallBack(action=4).pack()))
    array_buttons[3].append(InlineKeyboardButton(text='Регистр текста', callback_data=SetsCallBack(action=5).pack()))

    markup = InlineKeyboardMarkup(inline_keyboard=array_buttons)
    return markup
