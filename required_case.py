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
        return town
    else:
        raise Exception(f'Ошибка при запросе склонения: {response.status_code}')