modes_name = {
    'in': ['Мемас', 100],
    'de': ['Демотиватор', 101],
    'bo': ['Чтиво', 102],
    'fc': ['Факты', 103]
}
MODE_CODES_set = {mode[1] for mode in modes_name.values()}

COLORS = {
    'Нигер': ['#000000', 38],
    'Пурпурная пицца': ['#FF00FF', 39],
    'Баклажанный': ['#800080', 41],
    'Месячные': ['#FF0000', 42],
    'Детская неожиданность': ['#800000', 43],
    'Пись-пись': ['#FFFF00', 44],
    'Рвота': ['#808000', 45],
    'Вердепомовый': ['#00FF00', 46],
    'Индийский': ['#008000', 47],
    'Яйца странствующего дрозда': ['#00FFFF', 48],
    'Окраска птицы чюрок': ['#008080', 49],
    'Цвет уверенности': ['#0000FF', 51],
    'Форма морских офицеров': ['#000080', 52],
    'Белоснежка': ['#FFFFFF', 53],
}

SETTINGS_ACTION = -1
USERMODE_ACTION = 0
UPPERTEXT_ACTION = 1
BOTTOMTEXT_ACTION = 2
UPPERSTROKE_ACTION = 3
BOTTOMSTROKE_ACTION = 4
TEXTCASE_ACTION = 5
SETsmallcase = 6
SETgiantcase = 7
MAX_SYMBOLS = 500
MAX_SYMBOLS_GET_USERS = 800

COLOR_CODES_set = {color[1] * (10 ** power) for color in COLORS.values() for power in range(4)}


def get_colorhash_by_code(number, dictionary=None):
    if dictionary is None:
        dictionary = COLORS
    for key, value in dictionary.items():
        if value[1] == number:
            return value[0]
    return '#000000'


def get_colorname_by_hashcode(hash):
    for color_name, code_info in COLORS.items():
        if code_info[0] == hash:
            return color_name
    return hash


def get_mode_name_by_code(number, dictionary=None):
    if dictionary is None:
        dictionary = modes_name
    for key, value in dictionary.items():
        if value[1] == number:
            return key
    return None
