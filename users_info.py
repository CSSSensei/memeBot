import asyncio
import sqlite3
import json
from typing import Dict, List, Optional
import aiosqlite

users_db = 'users.db'
conn_loc = sqlite3.connect(users_db)
cursor_loc = conn_loc.cursor()

cursor_loc.execute('''CREATE TABLE IF NOT EXISTS users_info
                  (id INTEGER PRIMARY KEY, username TEXT DEFAULT NULL, mode TEXT DEFAULT 'in', banned BOOL DEFAULT False,
                  premium BOOL DEFAULT False, upper_color TEXT DEFAULT 'W', bottom_color TEXT DEFAULT 'W',
                  upper_stroke_color TEXT DEFAULT '-N', bottom_stroke_color TEXT DEFAULT '-N', stroke_width INTEGER DEFAULT 3,
                  giant_text BOOL DEFAULT False)''')
cursor_loc.close()
conn_loc.close()


class UserDB:
    def __init__(self, user_id, username=None, mode='in', banned=False, premium=False, upper_color='W', bottom_color='W',
                 upper_stroke_color='-N', bottom_stroke_color='-N', stroke_width=3, giant_text=False):
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
                    user = await UserDB.add_new_user(user_id, username)
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


if __name__ == "__main__":
    async def test():
        for user in await UserDB.get_users_from_db():
            print(user.__dict__)
    asyncio.run(test())

    # conn_loc = sqlite3.connect(users_db)
    # cursor_loc = conn_loc.cursor()
    #
    # cursor_loc.execute('SELECT * FROM users_info')
    # print(cursor_loc.fetchall())
    # cursor_loc.close()
    # conn_loc.close()
