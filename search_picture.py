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
    save_path = f'{os.path.dirname(__file__)}/pictures/{name}-{randint(1, 10 ** 9)}.png'

    if response.status_code == 200:
        bs = BeautifulSoup(response.content, 'html.parser')
        images = bs.find_all('img')
        images = images[3:]

        for i in range(len(images)):
            image = clean_link(str(choice(images)))
            if 'https://' in image:
                response = requests.get(image)
                if response.status_code == 200:
                    with open(save_path, 'wb') as file:
                        file.write(response.content)
                    return save_path
                else:
                    raise Exception(f'Ошибка при запросе картинки: {response.status_code}')

        raise Exception(f'Ошибка при скачивании картинки: {response.status_code}')

    else:
        raise Exception(f'Ошибка при поиске картинки: {response.status_code}')

