from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from config_data.modes_data import *
from callbacks.callback_info import *

meme_button: KeyboardButton = KeyboardButton(
    text='Мемас')
demotivator_button: KeyboardButton = KeyboardButton(
    text='Демотиватор')
book_button: KeyboardButton = KeyboardButton(
    text='Чтиво')
settings_button: KeyboardButton = KeyboardButton(
    text='Настройки')
basic_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[meme_button, demotivator_button], [book_button, settings_button]], resize_keyboard=True)


def get_keyboard():
    array_buttons: list[list[InlineKeyboardButton]] = [[], [], [], []]
    array_buttons[0].append(InlineKeyboardButton(text='Режим', callback_data=SetsCallBack(action=USERMODE_ACTION).pack()))
    array_buttons[1].append(InlineKeyboardButton(text='Цвет верхнего текста', callback_data=SetsCallBack(action=UPPERTEXT_ACTION).pack()))
    array_buttons[1].append(InlineKeyboardButton(text='Цвет нижнего текста', callback_data=SetsCallBack(action=BOTTOMTEXT_ACTION).pack()))
    array_buttons[2].append(InlineKeyboardButton(text='Контур верхнего текста', callback_data=SetsCallBack(action=UPPERSTROKE_ACTION).pack()))
    array_buttons[2].append(InlineKeyboardButton(text='Контур нижнего текста', callback_data=SetsCallBack(action=BOTTOMSTROKE_ACTION).pack()))
    array_buttons[3].append(InlineKeyboardButton(text='Регистр текста', callback_data=SetsCallBack(action=TEXTCASE_ACTION).pack()))

    markup = InlineKeyboardMarkup(inline_keyboard=array_buttons)
    return markup


def get_photo_inline_keyboard(photo_id):
    array_buttons: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text='Перегенерировать', callback_data=GenerateCallBack(photo_id=photo_id).pack())]]
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
