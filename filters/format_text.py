import re
import g4f
import asyncio
from config_data.config import bot

gpt_client = g4f.client.Client()


def find_first_number(input_string):
    match = re.search(r'\d+', input_string)

    if match:
        return match.group()
    else:
        return None


def format_string(text: str):
    if not text:
        return '⬛️'
    return text.replace('<', '«').replace('>', '»')


async def get_neuro_comment(message_text):
    response = gpt_client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user",
                   "content": f"Представь, что ты гопник. Объясни, что такое {message_text}, но говоря как некомпетентный человек и в дворовом стиле"}],
    )
    return response.choices[0].message.content


async def loading_indicator(chat_id, mes_id):
    clock = '🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛'
    cnt = 0
    while True:
        await bot.edit_message_text(chat_id=chat_id, message_id=mes_id,
                                    text=f'Секунду, братан, шестерёнки работают {clock[cnt % len(clock)]}')
        await asyncio.sleep(1)
        cnt += 1


def split_text(text, n):
    result = []
    lines = text.split('\n')
    current_chunk = ''
    current_length = 0

    for line in lines:
        if len(current_chunk) + len(line) + 1 <= n:  # Check if adding the line and '\n' fits in the chunk
            if current_chunk:  # Add '\n' if it's not the first line in the chunk
                current_chunk += '\n'
            current_chunk += line
            current_length += len(line) + 1
        else:
            result.append(current_chunk)
            current_chunk = line
            current_length = len(line)

    if current_chunk:
        result.append(current_chunk)

    return result
