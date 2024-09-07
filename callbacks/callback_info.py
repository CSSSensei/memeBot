from aiogram.filters.callback_data import CallbackData


class SetsCallBack(CallbackData, prefix="sets"):
    action: int


class GenerateCallBack(CallbackData, prefix="gen"):
    photo_id: int


class CutMessageCallBack(CallbackData, prefix="cut"):
    action: int
    user_id: int = 0
    page: int = 1
