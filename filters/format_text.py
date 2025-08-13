import asyncio
import re
from google import genai

from config_data.config import config


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
    client_AI = genai.Client(api_key=config.gemini_api_key)

    result = await asyncio.to_thread(
        client_AI.models.generate_content,
        model="gemini-2.5-flash",
        contents=f"Представь, что ты гопник. Объясни, что такое {message_text}, но говоря как некомпетентный человек и в дворовом стиле. "
                 f"Можешь использовать мат, не сдерживайся в выражениях"
    )
    return result.text


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
