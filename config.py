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

load_dotenv(find_dotenv())

API_TOKEN: str = os.getenv('TOKEN')
storage: MemoryStorage = MemoryStorage()

bot: Bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp: Dispatcher = Dispatcher(storage=storage)
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
    
import os
from mem_generator import create_meme




