import asyncio
import sqlite3
from typing import Dict, List, Optional, Union
import aiosqlite
import os

users_db = f'{os.path.dirname(__file__)}/DB/users.db'
conn_loc = sqlite3.connect(users_db)
cursor_loc = conn_loc.cursor()

cursor_loc.execute('''
    CREATE TABLE IF NOT EXISTS users_info (
        id INTEGER PRIMARY KEY,
        username TEXT DEFAULT NULL,
        mode TEXT DEFAULT 'in',
        banned BOOL DEFAULT False,
        premium BOOL DEFAULT False,
        upper_color TEXT DEFAULT '#FFFFFF',
        bottom_color TEXT DEFAULT '#FFFFFF',
        upper_stroke_color TEXT DEFAULT '#000000',
        bottom_stroke_color TEXT DEFAULT '#000000',
        stroke_width INTEGER DEFAULT 3,
        giant_text BOOL DEFAULT False
    )
''')
cursor_loc.execute('''
    CREATE TABLE IF NOT EXISTS UserQueries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        query TEXT
    )
''')
cursor_loc.close()
conn_loc.close()


class UserDB:
    def __init__(self, user_id, username=None, mode='in', banned=False, premium=False, upper_color='#FFFFFF', bottom_color='#FFFFFF',
                 upper_stroke_color='#000000', bottom_stroke_color='#000000', stroke_width=3, giant_text=False):
        self.user_id = user_id
        self.username = username
        self.mode = mode
        self.banned = banned
        self.premium = premium
        self.upper_color = upper_color
        self.bottom_color = bottom_color
        self.upper_stroke_color = upper_stroke_color
        self.bottom_stroke_color = bottom_stroke_color
        self.stroke_width = stroke_width
        self.giant_text = giant_text

    @classmethod
    async def get_users_from_db(cls, db_name: str = users_db) -> List['UserDB']:
        async with aiosqlite.connect(db_name) as db:
            cursor = await db.execute("SELECT * FROM users_info")
            rows = await cursor.fetchall()
            users = []
            for row in rows:
                user = cls(*row)
                users.append(user)
            return users

    @classmethod
    async def get_user(cls, user_id: Optional[int] = None, username: Optional[str] = None,
                       db_name: str = users_db) -> Optional['UserDB']:
        async with aiosqlite.connect(db_name) as db:
            if user_id:
                cursor = await db.execute("SELECT * FROM users_info WHERE id=?", (user_id,))
            elif username:
                cursor = await db.execute("SELECT * FROM users_info WHERE username=?", (username,))
            else:
                return None
            row = await cursor.fetchone()
            if row is None:
                if user_id:
                    user = await cls.add_new_user(user_id, username)
                    return user
                return None
            if username and user_id:
                await cls.upd_username(user_id, username)
            return cls(*row)

    @classmethod
    async def add_new_user(cls, user_id: int, username: Optional[str] = None,
                           db_name: str = users_db) -> 'UserDB':
        async with aiosqlite.connect(db_name) as db:
            cursor = await db.execute("SELECT * FROM users_info WHERE id=?", (user_id,))
            user_local = await cursor.fetchone()

            if user_local is None:
                await db.execute("INSERT INTO users_info (id, username) VALUES (?, ?)",
                                 (user_id, username))
                await db.commit()
                return cls(user_id, username)
            return cls(*user_local)

    @classmethod
    async def upd_username(cls, user_id: int, username: str, db_name: str = users_db) -> None:
        async with aiosqlite.connect(db_name) as db:
            try:
                await db.execute("UPDATE users_info SET username=? WHERE id=?", (username, user_id))
                await db.commit()
            except Exception as e:
                print(str(e))

    @classmethod
    async def change_mode(cls, user_id: int, mode, db_name: str = users_db) -> None:
        async with aiosqlite.connect(db_name) as db:
            try:
                await db.execute("UPDATE users_info SET mode=? WHERE id=?", (mode, user_id))
                await db.commit()
            except Exception as e:
                print(str(e))

    @classmethod
    async def change_color(cls, user_id: int, color: str, color_place: str, db_name: str = users_db) -> None:
        async with aiosqlite.connect(db_name) as db:
            try:
                if color_place in ('upper_color', 'bottom_color', 'upper_stroke_color', 'bottom_stroke_color'):
                    await db.execute(f"UPDATE users_info SET {color_place}=? WHERE id=?", (color, user_id))
                    await db.commit()
                else:
                    raise Exception(f'Неправильная команда смены цвета')
            except Exception as e:
                print(str(e))

    @classmethod
    async def change_text_case(cls, user_id: int, giant: bool, db_name: str = users_db) -> None:
        async with aiosqlite.connect(db_name) as db:
            try:
                await db.execute("UPDATE users_info SET giant_text=? WHERE id=?", (giant, user_id))
                await db.commit()
            except Exception as e:
                print(str(e))


class UserQueryDB:
    def __init__(self, user_id: int, queries: Union[Dict[int, str], None] = None):
        self.user_id: int = user_id
        self.queries: Union[Dict[int, str], None] = queries

    @classmethod
    async def add_new_query(cls, user_id: int, time: int, query: str, db_name: str = users_db):
        async with aiosqlite.connect(db_name) as db:
            await db.execute("INSERT INTO UserQueries (user_id, timestamp, query) VALUES (?, ?, ?)", (user_id, time, query))
            await db.commit()

    @classmethod
    async def get_user_queries(cls, user_id: int, db_name: str = users_db) -> 'UserQueryDB':
        async with aiosqlite.connect(db_name) as db:
            cursor: aiosqlite.Cursor = await db.execute(
                "SELECT timestamp, query FROM UserQueries WHERE user_id = ?", (user_id,)
            )
            rows: Union[list[tuple[int, str]], None] = await cursor.fetchall()
            queries: Union[Dict[int, str], None] = {row[0]: row[1] for row in rows} if rows else None
            return cls(user_id, queries)

    @classmethod
    async def get_last_queries(cls, amount: int, db_name: str = users_db) -> List['UserQueryDB']:
        async with aiosqlite.connect(db_name) as db:
            cursor = await db.execute(
                "SELECT user_id, timestamp, query FROM UserQueries ORDER BY timestamp DESC LIMIT ?",
                (amount,)
            )
            rows = await cursor.fetchall()
            query_objects = []
            for user_id, timestamp, query in rows:
                query_objects.append(cls(user_id, {timestamp: query}))
            return query_objects


if __name__ == "__main__":
    async def test():
        for user in await UserDB.get_users_from_db():
            print(user.__dict__)
        print(await UserDB.get_user(972753303, 'nklnkk'))


    async def test2():
        for user in await UserQueryDB.get_last_queries(5):
            print(user.__dict__)
        print((await UserQueryDB.get_user_queries(6149109321)).__dict__)


    # asyncio.run(test())
    asyncio.run(test2())

    # conn_loc = sqlite3.connect(users_db)
    # cursor_loc = conn_loc.cursor()
    #
    # cursor_loc.execute('SELECT * FROM users_info')
    # print(cursor_loc.fetchall())
    # cursor_loc.close()
    # conn_loc.close()
