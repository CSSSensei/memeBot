import os
import time
from aiogram import Router, F
import random
from DB.users_info import UserDB, UserQueryDB
from aiogram.types import Message, FSInputFile, InputMediaPhoto, CallbackQuery

from aiogram.utils.chat_action import ChatActionSender
from callbacks.callback_info import *
from keyboards import user_keyboards
from filters import filters, format_text
import asyncio
from config_data.config import bot, hz_answers
from config_data.modes_data import *
import mem_generator

router = Router()


@router.message(F.text, filters.ExplainBlyat())
async def explain_func(message: Message):
    required = 'поясни за '
    txt = message.text[len(required):]

    sent_message = await message.answer('Секунду, братан, шестерёнки работают')
    loading_task = asyncio.create_task(format_text.loading_indicator(sent_message.chat.id, sent_message.message_id))
    try:
        response = await format_text.get_neuro_comment(txt.replace("\n", " "))
        await message.answer(response, reply_markup=user_keyboards.basic_keyboard)
    finally:
        loading_task.cancel()
        await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


@router.message(F.text == 'Настройки')
async def settings_handler(message: Message, edit=False, user_id=None):
    user = await UserDB.get_user(user_id if user_id else message.from_user.id)
    #                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #                                          <--         phasalo          -->

    txt = ('<b>Твои текущие настройки</b>\n\n'
           f'Режим: <i><b>{modes_name[user.mode][0]}</b></i>\n'
           f'Цвет верхнего текста: <i><u>{get_colorname_by_hashcode(user.upper_color)}</u></i>\n'
           f'Цвет нижнего текста: <i><u>{get_colorname_by_hashcode(user.bottom_color)}</u></i>\n'
           f'Контур верхнего текста: <i><u>{get_colorname_by_hashcode(user.upper_stroke_color)}</u></i>\n'
           f'Контур нижнего текста: <i><u>{get_colorname_by_hashcode(user.bottom_stroke_color)}</u></i>\n'
           f'Регистр текста: <i>{"<b>БАЛЬШИЕ БУКАВЫ</b>" if user.giant_text else "маленькие буковки"}</i>\n')
    if edit:
        await message.edit_text(txt, reply_markup=user_keyboards.get_keyboard())
    else:
        await message.answer(txt, reply_markup=user_keyboards.get_keyboard())


@router.message(F.text == 'Демотиватор')
async def set_demotivator(message: Message):
    await UserDB.change_mode(message.from_user.id, 'de')
    await message.answer('Режим изменён на <b>демотиватор</b>', reply_markup=user_keyboards.basic_keyboard)


@router.message(F.text == 'Мемас')
async def set_meme(message: Message):
    await UserDB.change_mode(message.from_user.id, 'in')
    await message.answer('Режим изменён на <b>мемас</b>', reply_markup=user_keyboards.basic_keyboard)


@router.message(F.text == 'Чтиво')
async def set_book(message: Message, ):
    await UserDB.change_mode(message.from_user.id, 'bo')
    await message.answer('Режим изменён на <b>чтиво</b>', reply_markup=user_keyboards.basic_keyboard)


async def send_meme(message: Message, user: UserDB, mode=None, city_meme=False):
    async with ChatActionSender(bot=bot, chat_id=message.from_user.id, action='upload_photo'):
        try:
            if message.text is None and message.caption is None:
                await message.answer('Ты забыл про надпись')
                return
            meme_txt = message.text if message.text else message.caption
            photo_id = await UserQueryDB.add_new_query(user.user_id, int(time.time()), meme_txt)
            meme_txt = meme_txt.strip().split('\n')
            meme_txt[0] = meme_txt[0].replace('/', '').replace("\\", '')
            photo_path = None
            if city_meme:
                meme_txt = [None, None, None]
            if message.photo:
                photo_path = f'{os.path.dirname(__file__)}/pictures/photo{random.randint(1, 10 ** 8)}.jpg'
                await bot.download_file((await bot.get_file(message.photo[-1].file_id)).file_path, photo_path)

            try:
                meme_path = await mem_generator.create_meme(photo_path, *meme_txt,
                                                            mode=mode if mode else user.mode,
                                                            upper_color=user.upper_color,
                                                            bottom_color=user.bottom_color,
                                                            upper_stroke_color=user.upper_stroke_color,
                                                            bottom_stroke_color=user.bottom_stroke_color,
                                                            stroke_width=user.stroke_width,
                                                            giant_text=user.giant_text)

                keyboard = user_keyboards.basic_keyboard if (city_meme or message.photo) else user_keyboards.get_photo_inline_keyboard(photo_id)
                await message.answer_photo(photo=FSInputFile(meme_path), reply_markup=keyboard)
                os.remove(meme_path)
            except Exception as e:
                await message.answer('Что-то пошло не так', reply_markup=user_keyboards.basic_keyboard)
                await bot.send_message(chat_id=972753303, text=f'Произошла ошибка!\n{e}')
        except Exception as e:
            await message.answer('Что-то пошло не так', reply_markup=user_keyboards.basic_keyboard)
            await bot.send_message(chat_id=972753303, text=f'Произошла ошибка! Код 234\n{e}')


@router.callback_query(SetsCallBack.filter())
async def settings_button_distributor(callback: CallbackQuery, callback_data: SetsCallBack):
    action = callback_data.action
    user = await UserDB.get_user(callback.from_user.id, callback.from_user.username)

    async def user_mode(user_loc):
        current_mode_name = f"У вас включен режим: <b>{modes_name[user_loc.mode][0]}</b>"
        await callback.message.edit_text(current_mode_name, reply_markup=user_keyboards.get_mode_keyboard(user_loc.mode))

    async def color_mode(user_loc, action_loc):
        txt = ''
        mode_offset = 1
        current_color = '#000000'
        if action_loc == UPPERTEXT_ACTION:
            txt = 'верхнего текста'
            mode_offset = 1
            current_color = user_loc.upper_color
        elif action_loc == BOTTOMTEXT_ACTION:
            txt = 'нижнего текста'
            mode_offset = 10
            current_color = user_loc.bottom_color
        elif action_loc == UPPERSTROKE_ACTION:
            txt = 'контура верхнего текста'
            mode_offset = 100
            current_color = user_loc.upper_stroke_color
        elif action_loc == BOTTOMSTROKE_ACTION:
            txt = 'контура нижнего текста'
            mode_offset = 1000
            current_color = user_loc.bottom_stroke_color
        await callback.message.edit_text(f'Выберите цвет <i>{txt}</i> или введите его с клавиатуры',
                                         reply_markup=user_keyboards.get_color_keyboard(current_color, mode_offset))

    async def text_case_mode(user_loc):
        await callback.message.edit_text(f'Сейчас стоят {"<b>БАЛЬШИЕ БУКАВЫ</b>" if user_loc.giant_text else "<i>маленькие буковки</i>"}',
                                         reply_markup=user_keyboards.get_case_keyboard(user_loc.giant_text))

    if user is None:
        await callback.message.answer('Произошла ошибка!')

    if action == USERMODE_ACTION:
        await user_mode(user)

    if action in MODE_CODES_set:
        await UserDB.change_mode(callback.from_user.id, get_mode_name_by_code(action))
        user = await UserDB.get_user(callback.from_user.id, callback.from_user.username)
        await user_mode(user)

    if action == SETTINGS_ACTION:
        await settings_handler(callback.message, True, callback.from_user.id)
    if action in (UPPERTEXT_ACTION, BOTTOMTEXT_ACTION, UPPERSTROKE_ACTION, BOTTOMSTROKE_ACTION):
        await color_mode(user, action)

    if action in COLOR_CODES_set:
        color_places = ('upper_color', 'bottom_color', 'upper_stroke_color', 'bottom_stroke_color')
        color_codes = (UPPERTEXT_ACTION, BOTTOMTEXT_ACTION, UPPERSTROKE_ACTION, BOTTOMSTROKE_ACTION)
        offsets = {1000: 3, 100: 2, 10: 1}
        for div, idx in offsets.items():
            if action % div == 0:
                color_place = color_places[idx]
                command_name = color_codes[idx]
                offset = div
                break
        else:
            color_place = color_places[0]
            command_name = color_codes[0]
            offset = 1

        await UserDB.change_color(callback.from_user.id, get_colorhash_by_code(action // offset), color_place)
        user = await UserDB.get_user(callback.from_user.id, callback.from_user.username)
        await color_mode(user, command_name)
    if action == TEXTCASE_ACTION:
        await text_case_mode(user)
    if action in (SETgiantcase, SETsmallcase):
        await UserDB.change_text_case(callback.from_user.id, True if action == SETgiantcase else False)
        user = await UserDB.get_user(callback.from_user.id, callback.from_user.username)
        await text_case_mode(user)


@router.callback_query(GenerateCallBack.filter())
async def regenerate_button_distributor(callback: CallbackQuery, callback_data: GenerateCallBack):
    async with ChatActionSender(bot=bot, chat_id=callback.from_user.id, action='upload_photo'):
        photo_id = callback_data.photo_id
        query = await UserQueryDB.get_query_by_id(photo_id)
        meme_txt = query.strip().split('\n')
        meme_txt[0] = meme_txt[0].replace('/', '').replace("\\", '')
        user = await UserDB.get_user(user_id=callback.from_user.id, username=callback.from_user.username)
        meme_path = await mem_generator.create_meme(None, *meme_txt,
                                                    mode=user.mode,
                                                    upper_color=user.upper_color,
                                                    bottom_color=user.bottom_color,
                                                    upper_stroke_color=user.upper_stroke_color,
                                                    bottom_stroke_color=user.bottom_stroke_color,
                                                    stroke_width=user.stroke_width,
                                                    giant_text=user.giant_text)
        await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(meme_path)),
                                          reply_markup=user_keyboards.get_photo_inline_keyboard(photo_id))
        os.remove(meme_path)


@router.message(F.content_type.in_({'text', 'photo'}))
async def general_send_meme(message: Message):
    user = await UserDB.get_user(message.from_user.id, message.from_user.username)
    await send_meme(message, user)


@router.message()
async def any_message(message: Message):
    await message.answer(text=random.choice(hz_answers), reply_markup=user_keyboards.basic_keyboard)
