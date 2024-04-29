import re
import requests
import sqlite3
from time import sleep
from bs4 import BeautifulSoup
import os


EBAT = True
url = 'https://geoadm.com/'


db = f'{os.path.dirname(__file__)}/DB/towns.db'
conn = sqlite3.connect(db)
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS towns 
                  (name TEXT, used BOOL)''')


def write2db(word: str):
    cursor.execute("INSERT INTO towns (name, used) VALUES (?, ?)", (word, False))
    conn.commit()


def clean_link(link: str):
    ptrn = r'<a href="/(.*?)">(.*?)</a>'
    match = re.search(ptrn, link)
    if match:
        return f"{url}{match.group(1)}"
    else:
        return None


def taker(link):
    response = requests.get(link)
    if response.status_code == 200:
        bs = BeautifulSoup(response.text, "html.parser")
        table = bs.find_all('table')

        if len(table) == 2:
            table = table[1]
        else:
            table = table[0]
        rows = table.find_all('tr')[1:]

        for row in rows:
            cells = row.find_all('td')
            text, new_link = str(cells[0].text), clean_link(str(cells[0].a))

            if str(cells[0].text).isdigit():
                text = str(cells[1].text)
            write2db(text)

            if new_link:
                print("\033[34m{}\033[0m".format(new_link))
                if EBAT:
                    sleep(0.1)
                    taker(new_link)
            print("\033[33m{}\033[0m".format("=" * 100))
    else:
        raise Exception("\033[31m{}\033[0m".format(f"Ошибка при запросе города: {response.status_code}"))


if __name__ == '__main__':
    taker(url)

