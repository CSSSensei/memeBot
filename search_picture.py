import re
import requests
from random import choice, randint
from bs4 import BeautifulSoup
import os


def clean_link(link) -> str:
    pattern = r'src="(.*?)"'
    match = re.findall(pattern, link)
    # print(match[0])
    return match[0]


def search_picture(name: str):
    response = requests.get(f'https://www.google.com/search?q={name}&tbm=isch')
    rand_int = randint(1, 10 ** 9)

    if response.status_code == 200:
        bs = BeautifulSoup(response.content, 'html.parser')
        images = bs.find_all('img')
        images = images[3:]

        for i in range(len(images)):
            image = clean_link(str(choice(images)))
            if 'https://' in image:
                response = requests.get(image)
                if response.status_code == 200:
                    with open(f'{os.path.dirname(__file__)}/pictures/{name}{rand_int}.png', 'wb') as file:
                        file.write(response.content)
                    return f'{os.path.dirname(__file__)}/pictures/{name}{rand_int}.png'
                else:
                    raise Exception('\033[33m{}\033[0m'.format(f'Ошибка при запросе картинки: {response.status_code}'))

        raise Exception('\033[33m{}\033[0m'.format(f'Ошибка при скачивании картинки: {response.status_code}'))

    else:
        raise Exception('\033[33m{}\033[0m'.format(f'Ошибка при поиске картинки: {response.status_code}'))

