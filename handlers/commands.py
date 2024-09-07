from aiogram.filters import Command, CommandStart
import os
from aiogram import Router, F
from keyboards import user_keyboards
from aiogram.types import Message
from DB.users_info import UserDB
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import FSInputFile, InputMediaPhoto
from config_data.config import bot
from handlers.user_handlers import send_meme

router = Router()


@router.message(CommandStart())  # /start
async def process_start_command(message: Message):
    await UserDB.add_new_user(message.from_user.id, message.from_user.username)
    await message.answer(
        'Здарова! Тут ты можешь подавить лыбу 🤣🤣🤣\n\nТыкай на <b>/help</b> чтобы узнать, как пользоваться хи-хи ха-ха ботом 👍',
        reply_markup=user_keyboards.basic_keyboard)


@router.message(Command(commands='meme'))  # /meme
async def send_meme_lmao(message: Message):
    await send_meme(message, user=await UserDB.get_user(message.from_user.id, message.from_user.username), mode='in', city_meme=True)


@router.message(Command(commands='help'))  # /help
async def help_command(message: Message):
    await message.answer('<b>Помощь калекам</b>\n'
                         'Для создания реальной ржаки тебе нужно нажать на кнопочки снизу (Выбрать шаблон <i>/example</i>)\n\n'
                         '<i><b>«Мемас» и «демотиватор»</b></i>\n'
                         'Пишешь текст сверху, текст снизу и запрос на картинку.\n'
                         '<b>Всё с новой строчки!</b> (Shift + Enter)\n'
                         'Запрос на картинку пиши, как будто в гугле картинку ищешь\n'
                         '<blockquote>Надпись сверху\n'
                         'Надпись снизу\n'
                         'Запрос на картинку</blockquote>\n\n'
                         'Так же ты можешь прислать фотку вместо запроса и подписать её: текст сверху и текст снизу'
                         '<blockquote>Надпись сверху\n'
                         'Надпись снизу</blockquote>\n\n'
                         'Можно не присылать два текста'
                         '<blockquote>Надпись\n'
                         'Запрос на картинку</blockquote>\n\n'
                         'Или вообще одну надпись'
                         '<blockquote>Надпись</blockquote>\n\n'
                         '<i><b>«Чтиво»</b></i>\n'
                         '<blockquote>Автор (ФИО)\n'
                         'Название\n'
                         'Запрос на картинку</blockquote>\n', reply_markup=user_keyboards.basic_keyboard)


@router.message(Command(commands='example'))  # /example
async def example_command(message: Message):
    assets_directory = os.path.join(os.path.dirname(__file__), os.pardir, 'assets')

    async with ChatActionSender(bot=bot, chat_id=message.from_user.id, action='upload_photo'):
        photo1 = InputMediaPhoto(media=FSInputFile(os.path.join(assets_directory, 'example1.jpg')))
        photo2 = InputMediaPhoto(media=FSInputFile(os.path.join(assets_directory, 'example2.jpg')))
        photo3 = InputMediaPhoto(media=FSInputFile(os.path.join(assets_directory, 'example3.jpg')))

        await bot.send_media_group(media=[photo1, photo2, photo3], chat_id=message.chat.id)


@router.message(Command(commands='about'))  # /about
async def about_command(message: Message):
    await message.answer('<i>Команда Phasalopedia. 16+\n2024</i>\n\nПоддержка:\n<b>@nklnkk</b>', reply_markup=user_keyboards.basic_keyboard)


@router.message(Command(commands='deme'))  # /deme
async def create_demo_command(message: Message):
    await send_meme(message, user=await UserDB.get_user(message.from_user.id, message.from_user.username), mode='de', city_meme=True)


@router.message(Command(commands='book'))  # /book
async def create_demo_command(message: Message):
    await send_meme(message, user=await UserDB.get_user(message.from_user.id, message.from_user.username), mode='bo')
