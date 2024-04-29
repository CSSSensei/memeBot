import os
from search_picture import search_picture
from required_case import word2case
from creation_picture import create_insult, create_demotiv
from taker_from_db import take_from_db
from random import choice, shuffle, randint
import asyncio


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


async def create_meme(path_img: str = None,
                      search_text: str = None,
                      upper_text: str = None,
                      bottom_text: str = None,
                      mode='in'):  # in, de

    mem_search_text = search_text if search_text \
        else await take_from_db()

    mem_path_img = path_img if path_img \
        else await search_picture(mem_search_text)

    mem_upper_text = upper_text if upper_text \
        else f"Жители {await word2case(mem_search_text, 'Р')}"

    mem_bottom_text = bottom_text if bottom_text \
        else random_insult()

    if mode == 'in':
        path_mem = create_insult(mem_path_img,
                                 mem_upper_text,
                                 mem_bottom_text)
    elif mode == 'de':
        path_mem = create_demotiv(mem_path_img,
                                  mem_upper_text,
                                  mem_bottom_text)
    else:
        return mem_path_img

    os.remove(mem_path_img)
    return path_mem
