from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass
import os
from aiogram import Bot

load_dotenv(find_dotenv())


@dataclass
class TgBot:
    token: str = os.getenv('TOKEN')
    message_max_symbols: int = 4096


@dataclass
class Config:
    tg_bot: TgBot
    gemini_api_key: str = os.getenv('GEMINI_API_KEY')


def load_config(path: str | None = None) -> Config:
    return Config(tg_bot=TgBot())


config: Config = load_config()

bot = Bot(token=config.tg_bot.token, parse_mode="HTML")

hz_answers = ['Я тебя не понимаю...', 'Я не понимаю, о чем ты', 'Что ты имеешь в виду? 🧐', 'Я в замешательстве 🤨',
              'Не улавливаю смысла 🙃', 'Что ты пытаешься сказать❓', 'Не понимаю твоего сообщения 😕',
              '🤷‍♂️ Не понимаю 🤷‍♀️']

if __name__ == '__main__':
    pass
