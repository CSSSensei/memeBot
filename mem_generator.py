import os
import re
from random import choice, shuffle
import asyncio

from search_picture import search_picture
from required_case import word2case
from taker_from_db import take_from_db
from creation_picture import *


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


def decoding_color(init_color: str) -> str:
    default_color = '#000000'
    pattern = r'^#[0-9a-fA-F]{6}$'

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

    color = init_color.replace(" ", "")

    if len(color) == 1:
        if color.isalpha() and color in letter2color.keys():
            return letter2color[color.upper()]
        return default_color

    color = color.ljust(7, '0')

    if re.match(pattern, color) is not None:
        return color
    return default_color


def random_color4book() -> str:
    color = [  # Я заебался вычленять эти цвета (Надеюсь будет работать)
        '#2d3c54', '#647047', '#e6b327',
        '#781416', '#c41f25', '#519876',
        '#ca5300', '#4a546a', '#7c918f',
        '#68959a', '#00557a', '#587697',
        '#816069', '#2e162a', '#5d5971',
        '#b5687b', '#73928a', '#003a58',
        '#d18004', '#75a8ad', '#7ca676',
        '#ca0707', '#77c5cd', '#a79700',
        '#d57900', '#421a15', '#666127',
        '#3d3926', '#827c5e', '#df735a',
        '#24a09b', '#a2433d', '#7e835d',
        '#fdae10', '#958f00', '#2e5e45',
        '#1b3d3f', '#d84d1c', '#f09d28',
        '#b1b278', '#6e2368', '#bf9e4a',
        '#b6a65e', '#7c190f', '#8e986a',
        '#ea8924', '#890d15', '#ccaa01',
        '#c46a02', '#9f9b05', '#e76202',
        '#286f30', '#eca406', '#753650',
        '#3e7b72', '#99022f', '#8f8a1c',
        '#374702', '#8f8a1c', '#ce5800',
        '#32550a', '#dca500', '#c5b402',
        '#63484b', '#a08d86', '#dc511c',
        '#3977ae', '#bf2829', '#69ad3f',
        '#f7b62f', '#439885', '#015868',
        '#e18805', '#d7b604', '#206a6a',
        '#942c1b', '#91703e', '#7b512c',
        '#aba047', '#004870', '#8b9848',
        '#822b0d', '#1f2849', '#9b1120',
        '#1379bb', '#bcbcbc', '#0d6370',
        '#209ed9', '#e9ad31', '#c8af31',
        '#c32621', '#3a805c', '#704b5d',
        '#a2a135', '#0c404d', '#ebb932',
        '#507e74', '#b57933', '#244256',
        '#00a678', '#134b6d', '#5ba49b',
        '#7d797a', '#e0827a', '#029fa6',
        '#364c86', '#7f1313', '#01928d',
        '#8c1519', '#dc6708', '#70a595',
        '#7a3142', '#d96125', '#e9836d',
        '#851124', '#e59204', '#834436',
        '#184e2c', '#b17247', '#076f65',
        '#b55c20', '#7a3c1b', '#c24d3c',
        '#682e4b', '#682e4b', '#af6a43',
        '#682e4b', '#682e4b', '#08acdf',
        '#9f3422', '#7d0e14', '#054865',
        '#455a39', '#aa9e56', '#c17230',
        '#aa880b', '#444f25', '#617ca9',
        '#033964', '#d24332', '#6a333c',
        '#df2063', '#8a0b52', '#918d4d',
        '#526421', '#d9a627', '#5b1a1c',
        '#a21a26', '#1f4354', '#eca702',
        '#b8ca02', '#094666', '#468c33'
    ]
    return choice(color)


async def create_meme(path_img: str = None,
                      bottom_text: str = None,
                      upper_text: str = None,
                      search_text: str = None,
                      mode='in',  # in, de, bo
                      upper_color='W',
                      bottom_color='W',
                      upper_stroke_color='-N',   # Тут нет ошибки!
                      bottom_stroke_color='-N',  # '-N' — это код стандартного цвета (чёрного)
                      stroke_width=3,
                      giant_text=False):
    size = 1000
    distance = 50

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
        mem_upper_text = mem_bottom_text
        mem_bottom_text = upper_text
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
                                 upper_text=mem_upper_text.upper(),
                                 bottom_text=mem_bottom_text.upper(),
                                 upper_color=decoding_color(upper_color),
                                 bottom_color=decoding_color(bottom_color),
                                 upper_stroke_color=decoding_color(upper_stroke_color),
                                 bottom_stroke_color=decoding_color(bottom_stroke_color),
                                 stroke_width=stroke_width,
                                 giant_text=giant_text,
                                 size=size,
                                 distance=distance)

    elif mode == 'de':

        if bottom_text and not upper_text:
            mem_upper_text = bottom_text
            mem_bottom_text = ''

        # if upper_stroke_color != '-N':
        #     stroke_color = upper_stroke_color
        # elif bottom_stroke_color != '-N':
        #     stroke_color = bottom_stroke_color
        # else:
        stroke_color = 'W'

        path_mem = create_demotiv(path=mem_path_img,
                                  upper_text=mem_upper_text,
                                  bottom_text=mem_bottom_text,
                                  footnote='phasalopedia.ru',
                                  upper_color=decoding_color(upper_color),
                                  bottom_color=decoding_color(bottom_color),
                                  stroke_color=decoding_color(stroke_color),
                                  stroke_width=stroke_width,
                                  size=size,
                                  distance=distance)

    elif mode == 'bo':
        upper_stroke_color = random_color4book()
        bottom_stroke_color = random_color4book()

        # if upper_stroke_color == '-N':
        #     upper_stroke_color = random_color4book()
        # if bottom_stroke_color == '-N':
        #     bottom_stroke_color = random_color4book()

        logo_backing_color = choice([
            '#fdd260', '#eb8924', '#79a4aa',
            '#faef9f', '#c7a74e', '#b6a65d',
            '#b16679', '#d34e19', '#e27c68'])

        if len(mem_upper_text.split()) > 3:
            mem_upper_text = " ".join(mem_upper_text.split()[:3])

        size = 600
        distance = 60
        descriptor = choice(['эксклюзивная классика', 'русская классика'])
        annotation_location = choice(['l', 'r'])

        path_mem = create_book(path=mem_path_img,
                               author=mem_upper_text.upper(),
                               title=mem_bottom_text.upper(),
                               descriptor=descriptor,
                               annotation_location=annotation_location,
                               annotation=['Книги, изменившие мир.',
                                           'Писатели, объединившие',
                                           'поколения.'],
                               author_backing_color=decoding_color(upper_stroke_color),
                               title_backing_color=decoding_color(bottom_stroke_color),
                               logo_backing_color=decoding_color(logo_backing_color),
                               size=size,
                               distance=distance)
    else:
        return mem_path_img

    os.remove(mem_path_img)
    return path_mem


if __name__ == '__main__':
    asyncio.run(
        create_meme(
            # path_img="pictures/1.jpg",
            path_img=None,
            bottom_text="я оказывается пассивный латентный гетеросексуал",
            # bottom_text="1985",
            # bottom_text="Горе от ума",
            # bottom_text="Вероника решает умереть",
            # upper_text="Пауло коэльо",
            # upper_text="Ирвин жопэ Шоу",
            # upper_text="Харпер ли",
            upper_text="гей",
            # upper_text="Хуй сергеевич",
            # upper_text=None,
            search_text=None,
            mode='bo',
            upper_color='#588157',
            bottom_color='#588157',
            # upper_stroke_color="#c1121f",
            # bottom_stroke_color="#2d3a53",
            stroke_width=4,
            giant_text=False
        )
    )
