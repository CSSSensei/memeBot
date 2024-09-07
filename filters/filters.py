from aiogram.filters import BaseFilter
from aiogram.types import Message

ADMINS = (972753303, 735273809)


class AdminUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS


class ExplainBlyat(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        required = 'поясни за '
        return message.text[0:len(required)].lower() == required
