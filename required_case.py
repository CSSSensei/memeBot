import requests
import json

url = 'https://ws3.morpher.ru/russian/declension'


def word2case(town: str, case: str) -> str:

    headers = {'User-Agent': 'TG'}

    params = {
        's': town,
        'format': 'json',
    }

    response = requests.get(url=url,
                            params=params,
                            headers=headers)

    data = json.loads(response.text)

    if response.status_code == 200:
        return data.get(case)
    elif response.status_code == 402:
        raise Exception('\033[33m{}\033[0m'.format(f'Закончилось количество запросов спряжения'))
    else:
        raise Exception('\033[33m{}\033[0m'.format(f'Ошибка при запросе склонения: {response.status_code}'))