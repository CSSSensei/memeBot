import re
from aiohttp import ClientSession
from random import choice, randint
from bs4 import BeautifulSoup
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def clean_link(link) -> str:
    pattern = r'src="(.*?)"'
    match = re.findall(pattern, link)
    # print(match[0])
    return match[0]


async def fetch_image(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            image_data = await response.read()
            return image_data
        else:
            raise Exception(f'Ошибка при запросе картинки: {response.status}')


async def search_picture(name: str):
    async with ClientSession() as session:
        url = f'https://www.google.com/search?q={name}&tbm=isch'
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                bs = BeautifulSoup(await response.text(), 'html.parser')
                images = bs.find_all('img')[3:]

                for _ in range(len(images)):
                    image = clean_link(str(choice(images)))
                    if 'https://' in image:
                        image_data = await fetch_image(session, image)
                        save_path = f'{os.path.dirname(__file__)}/pictures/{name}-{randint(1, 10 ** 9)}.png'
                        with open(save_path, 'wb') as file:
                            file.write(image_data)
                        return save_path

                raise Exception('Картинки не найдены или не удалось загрузить')

            else:
                raise Exception(f'Ошибка при поиске картинки: {response.status}')
