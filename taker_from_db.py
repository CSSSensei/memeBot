import asyncio
import aiosqlite
import sqlite3
import os

townsDB = f'{os.path.dirname(__file__)}/DB/towns.db'


async def take_from_db():
    async with aiosqlite.connect(townsDB) as db:
        cursor = await db.execute('SELECT name FROM towns WHERE used = False ORDER BY RANDOM() LIMIT 1')
        town = await cursor.fetchone()
        if not town:
            return None
        return town[0]


def print_db():
    db = f'{os.path.dirname(__file__)}/DB/towns.db'
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('SELECT * from towns')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print(len(rows))
    cursor.close()
    conn.close()


if __name__ == '__main__':
    print(asyncio.run(take_from_db()))
