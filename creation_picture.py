from PIL import Image, ImageDraw, ImageFont
import os


def create_insult(path: str,
                  upper_text: str,
                  bottom_text: str,
                  size: int = 1000,
                  distance: int = 50) -> str:
    save_path = f'{path[:-4]}-mem-insult.png'
    text_size = size // 10

    img = Image.open(path).convert('RGB')
    img = img.resize((size, size))
    img_cnv = ImageDraw.Draw(img)

    font = ImageFont.truetype(f'{os.path.dirname(__file__)}/assets/Impact.ttf', text_size)
    text_width_upper = img_cnv.textlength(upper_text, font=font)
    text_width_bottom = img_cnv.textlength(bottom_text, font=font)

    while (text_width_upper >= size - (distance * 2) or
           text_width_bottom >= size - (distance * 2)) and \
            (text_size != 1):
        text_size = text_size - 1 if text_size - 1 > 0 else 1
        font = ImageFont.truetype(f'{os.path.dirname(__file__)}/assets/Impact.ttf', text_size)
        text_width_upper = img_cnv.textlength(upper_text, font=font)
        text_width_bottom = img_cnv.textlength(bottom_text, font=font)

    img_cnv.text((size // 2, distance),
                 upper_text.upper(),
                 font=font,
                 fill=(255, 255, 255),
                 stroke_width=7,
                 stroke_fill=(0, 0, 0),
                 anchor="mt"
                 )
    img_cnv.text((size // 2, size - distance),
                 bottom_text.upper(),
                 font=font,
                 fill=(255, 255, 255),
                 stroke_width=7,
                 stroke_fill=(0, 0, 0),
                 anchor="ms"
                 )

    img.save(save_path)
    return save_path


def create_demotiv(path: str,
                   upper_text: str,
                   bottom_text: str,
                   footnote: str = 'phasalopedia.ru',
                   size: int = 1000,
                   distance: int = 50) -> str:
    save_path = f'{path[:-4]}-mem-demotiv.png'
    text_size = size // 10

    img = Image.new('RGB', (size, size), color=(0, 0, 0))
    img_cnv = ImageDraw.Draw(img)

    font_upper = ImageFont.truetype(f'{os.path.dirname(__file__)}/assets/Times New Roman.ttf', text_size)
    font_bottom = ImageFont.truetype(f'{os.path.dirname(__file__)}/assets/Arial.ttf', text_size // 2)
    text_width_upper = img_cnv.textlength(upper_text, font=font_upper)
    text_width_bottom = img_cnv.textlength(bottom_text, font=font_bottom)

    while (text_width_upper >= size - (distance * 4) or
           text_width_bottom >= size - (distance * 4)) and \
            (text_size != 1):
        text_size = text_size - 1 if text_size - 1 > 0 else 1
        font_upper = ImageFont.truetype(f'{os.path.dirname(__file__)}/assets/Times New Roman.ttf', text_size)
        font_bottom = ImageFont.truetype(f'{os.path.dirname(__file__)}/assets/Arial.ttf', text_size // 2)
        text_width_upper = img_cnv.textlength(upper_text, font=font_upper)
        text_width_bottom = img_cnv.textlength(bottom_text, font=font_bottom)

    # отношение высоты буквы к размеру шрифта:
    # Arial: 0.74
    # Times New Roman: 0.68

    font_footnote = ImageFont.truetype(f'{os.path.dirname(__file__)}/assets/Times New Roman.ttf', 23)

    img_cnv.rectangle((distance // 1.2, distance // 1.2,
                       size - distance // 1.2, int(size - 2.33334 * distance - 1.05 * text_size)),
                      fill=(0, 0, 0, 0),
                      outline=(255, 255, 255),
                      width=3,
                      )

    img_past = Image.open(path).convert('RGB')
    img_past = img_past.resize((size - (distance * 2), int(size - 3.5 * distance - 1.05 * text_size)))
    img.paste(img_past, (distance, distance))

    img_cnv.text((size // 2, size - int(1.25 * distance) - text_size // 2),
                 upper_text,
                 font=font_upper,
                 fill=(255, 255, 255),
                 anchor="ms"
                 )
    img_cnv.text((size // 2, size - distance),
                 bottom_text,
                 font=font_bottom,
                 fill=(255, 255, 255),
                 anchor="ms"
                 )
    bbox = img_cnv.textbbox((size - 1.08 * distance, int(size - 2.33334 * distance - 1.05 * text_size)),
                            footnote,
                            font=font_footnote,
                            anchor="rm")
    img_cnv.rectangle(bbox, fill=(0, 0, 0))

    img_cnv.text((size - 1.08 * distance, int(size - 2.33334 * distance - 1.05 * text_size)),
                 footnote,
                 font=font_footnote,
                 fill=(255, 255, 255),
                 stroke_fill=(0, 0, 0),
                 anchor="rm"
                 )

    img.save(save_path)
    return save_path

# create_picture('pictures/Коты.png', 'Сиси')
# create_picture('pictures/Коты.png', 'Кременчуг-Константиновского')

# for x in range(upper_x, upper_x + text_width_upper):
#     for y in range(upper_y, upper_y + text_size):
#         if x < size and y < size:
#             img.putpixel((x, y), (255, 0, 0))
#
# for x in range(bottom_x, bottom_x + text_width_bottom):
#     for y in range(bottom_y, bottom_y + text_size):
#         if x < size and y < size:
#             img.putpixel((x, y), (255, 0, 0))
#
# for x in range(distance, size - distance, 4):
#     for y in range(distance, size - distance, 4):
#         img.putpixel((x, y), (0, 0, 0))
#
# for y in range(0, size, 4):
#     img.putpixel((size // 2, y), (0, 0, 222))

# img_cnv.line([(0, size - distance), (size, size - distance)],
#              fill=(255, 0, 0),
#              width=1)
#
# img_cnv.line([(0, size - distance - text_size * 0.74 // 2), (size, size - distance - text_size * 0.74 // 2)],
#              fill=(255, 0, 0),
#              width=1)
#
# img_cnv.line([(0, size - 1.5 * distance - text_size * 0.74 // 2), (size, size - 1.5 * distance - text_size * 0.74 // 2)],
#              fill=(255, 0, 0),
#              width=1)
#
# img_cnv.line(
#     [(0, size - 1.5 * distance - text_size * 0.74 // 2 - text_size * 0.68), (size, size - 1.5 * distance - text_size * 0.74 // 2 - text_size * 0.68)],
#     fill=(255, 0, 0),
#     width=1)
