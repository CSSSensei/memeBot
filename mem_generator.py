import os
from search_picture import search_picture
from required_case import word2case
from creation_picture import *
from taker_from_db import take_from_db
from random import choice, shuffle


def random_insult() -> str:
    list1 = ['там',
             '',
             ]
    list2 = ['нахуй',
             'чтоли',
             'чтоль',
             'пиздец',
             'ебать',
             'блять',
             '',
             ]
    list3 = ['совсем',
             'абсолютно',
             'совершенно',
             '',
             ]
    list4 = ['ёбнулись', 'ёбнутые',
             'охуели', 'охуевшие',
             'охнели', 'охневшие',
             'ахуели', 'ахуевшие',
             'ахнели', 'ахневшие',
             'офигели', 'офигевшие',
             'прихуели', 'прихуевшие',
             'прихнели', 'прихневшие',
             'прифигели', 'прифигевшие',
             'очешуели', 'очешуевшие',
             'долбанулись', 'долбанутые',
             'конченые',
             ]

    insult = [choice(list1), choice(list2), choice(list3), choice(list4)]
    shuffle(insult)
    str_insult = ' '.join(insult).replace('  ', ' ').strip()
    return f'Вы {str_insult}?'


def decoding_color(color: str):
    default_color = '#000000'

    letter2color = {'F': '#FF00FF',
                    'P': '#800080',
                    'R': '#FF0000',
                    'M': '#800000',
                    'Y': '#FFFF00',
                    'O': '#808000',
                    'L': '#00FF00',
                    'G': '#008000',
                    'A': '#00FFFF',
                    'T': '#008080',
                    'B': '#0000FF',
                    'N': '#000080',
                    'W': '#FFFFFF'}

    color = color.strip()
    color = color.replace(" ", "")

    if len(color) == 1:
        if color.isalpha() and color in letter2color.keys():
            return letter2color[color.upper()]
        return default_color
    elif color[0] == '#':
        if color[1:].isdigit():
            return f'#{color[1:].zfill(6)}'
        return default_color
    return default_color


def random_descriptor() -> str:
    return choice(['эксклюзивная классика', 'русская классика'])


def random_color4book() -> str:
    return choice(['эксклюзивная классика', 'русская классика'])


async def create_meme(path_img: str = None,
                      bottom_text: str = None,
                      upper_text: str = None,
                      search_text: str = None,
                      mode='in',  # in, de, bo
                      upper_color='W',
                      bottom_color='W',
                      upper_stroke_color='-N',  # Тут нет ошибки!
                      bottom_stroke_color='-N',  # '-N' — это код стандартного цвета (чёрного)
                      stroke_width=3,
                      giant_text=False,
                      size=1000,
                      distance=50):
    path_img = None if path_img == '' else path_img
    bottom_text = None if bottom_text == '' else bottom_text
    search_text = None if search_text == '' else search_text

    if bottom_text:
        mem_bottom_text = bottom_text
    else:
        mem_bottom_text = random_insult()

    if search_text:
        mem_search_text = search_text
    elif bottom_text:
        mem_search_text = bottom_text
    else:
        mem_search_text = await take_from_db()

    if upper_text:
        mem_upper_text = upper_text
    elif bottom_text:
        mem_upper_text = ''
    else:
        mem_upper_text = f"Жители {await word2case(mem_search_text, 'Р')}"

    if path_img:
        mem_path_img = path_img
    else:
        mem_path_img = await search_picture(mem_search_text)

    if mode == 'in':
        path_mem = create_insult(path=mem_path_img,
                                 upper_text=mem_upper_text,
                                 bottom_text=mem_bottom_text,
                                 upper_color=decoding_color(upper_color),
                                 bottom_color=decoding_color(bottom_color),
                                 upper_stroke_color=decoding_color(upper_stroke_color),
                                 bottom_stroke_color=decoding_color(bottom_stroke_color),
                                 stroke_width=stroke_width,
                                 giant_text=giant_text,
                                 size=size,
                                 distance=distance)

    elif mode == 'de':
        path_mem = create_demotiv(path=mem_path_img,
                                  upper_text=mem_upper_text,
                                  bottom_text=mem_bottom_text,
                                  footnote='phasalopedia.ru',
                                  upper_color=decoding_color(upper_color),
                                  bottom_color=decoding_color(bottom_color),
                                  size=size,
                                  distance=distance)

    elif mode == 'bo':

        if upper_stroke_color == '-N':
        if bottom_stroke_color == '-N':

        path_mem = create_book(path=mem_path_img,
                               author=mem_upper_text,
                               title=mem_bottom_text,
                               descriptor=random_descriptor(),
                               author_backing_color=decoding_color(upper_stroke_color),
                               title_backing_color=decoding_color(bottom_stroke_color),
                               size=size)
    else:
        return mem_path_img

    os.remove(mem_path_img)
    return path_mem


if __name__ == '__main__':
    print(decoding_color('        # 955494       '))
