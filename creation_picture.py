from PIL import Image, ImageDraw, ImageFont
import os


def create_insult(path: str,
                  upper_text: str,
                  bottom_text: str,
                  upper_color: str,
                  bottom_color: str,
                  upper_stroke_color: str,
                  bottom_stroke_color: str,
                  stroke_width: int,
                  giant_text: bool,
                  size: int,
                  distance: int) -> str:
    save_path = f'{path[:-4]}-mem-insult.png'
    text_size = size if giant_text else size // 10
    impact = f'{os.path.dirname(__file__)}/assets/Impact.ttf'

    img = Image.open(path).convert('RGB').resize((size, size))
    img_cnv = ImageDraw.Draw(img)

    font = ImageFont.truetype(impact, text_size)
    text_width_upper = img_cnv.textlength(upper_text, font=font)
    text_width_bottom = img_cnv.textlength(bottom_text, font=font)

    while (text_width_upper >= size - (distance * 2) or
           text_width_bottom >= size - (distance * 2)) and \
            (text_size != 1):
        text_size = text_size - 1 if text_size - 1 > 0 else 1
        font = ImageFont.truetype(impact, text_size)
        text_width_upper = img_cnv.textlength(upper_text, font=font)
        text_width_bottom = img_cnv.textlength(bottom_text, font=font)

    img_cnv.text((size // 2, distance),
                 upper_text,
                 font=font,
                 fill=upper_color,
                 stroke_width=stroke_width,
                 stroke_fill=upper_stroke_color,
                 anchor="mt"
                 )
    img_cnv.text((size // 2, size - distance),
                 bottom_text,
                 font=font,
                 fill=bottom_color,
                 stroke_width=stroke_width,
                 stroke_fill=bottom_stroke_color,
                 anchor="ms"
                 )

    img.save(save_path)
    return save_path


def create_demotiv(path: str,
                   upper_text: str,
                   bottom_text: str,
                   footnote: str,
                   upper_color: str,
                   bottom_color: str,
                   stroke_color: str,
                   stroke_width: int,
                   size: int,
                   distance: int) -> str:
    save_path = f'{path[:-4]}-mem-demotiv.png'
    text_size = size // 10
    times_new_roman = f'{os.path.dirname(__file__)}/assets/Times New Roman.ttf'
    arial = f'{os.path.dirname(__file__)}/assets/Arial.ttf'

    img_past = Image.open(path).convert('RGB')
    relation = img_past.height / img_past.width

    img_past = img_past.resize((size - (distance * 2), int((size - (distance * 2)) * relation)))

    img = Image.new('RGB', (size, size), color="#000000")
    img_cnv = ImageDraw.Draw(img)

    font_upper = ImageFont.truetype(times_new_roman, text_size)
    font_bottom = ImageFont.truetype(arial, text_size // 2)
    text_width_upper = img_cnv.textlength(upper_text, font=font_upper)
    text_width_bottom = img_cnv.textlength(bottom_text, font=font_bottom)

    while (text_width_upper >= img.width - (distance * 4) or
           text_width_bottom >= img.width - (distance * 4)) and \
            (text_size != 1):
        text_size = text_size - 1 if text_size - 1 > 0 else 1
        font_upper = ImageFont.truetype(times_new_roman, text_size)
        font_bottom = ImageFont.truetype(arial, text_size // 2)
        text_width_upper = img_cnv.textlength(upper_text, font=font_upper)
        text_width_bottom = img_cnv.textlength(bottom_text, font=font_bottom)

    font_footnote = ImageFont.truetype(times_new_roman, 25)

    # TODO:
    #  Отношение высоты буквы к размеру шрифта:
    #  Arial: 0.74
    #  Times New Roman: 0.68

    if bottom_text == '':
        img = img.resize((img.width, int(3 * distance + img_past.height + 0.68 * text_size)))
    else:
        img = img.resize((img.width, int(3.25 * distance + img_past.height + 1.05 * text_size)))

    img_cnv = ImageDraw.Draw(img)

    img_cnv.rectangle((distance - 8,
                       distance - 8,
                       img_past.width + distance + 8,
                       img_past.height + distance + 8),
                      fill='#000000',
                      outline=stroke_color,
                      width=stroke_width,
                      )

    img.paste(img_past, (distance, distance))

    bbox = img_cnv.textbbox((int(img_past.width + distance - 1),
                             int(img_past.height + distance)),
                            footnote,
                            font=font_footnote,
                            anchor='rt')

    bbox = list(bbox)
    bbox[0] -= 4
    bbox[2] += 4
    bbox = tuple(bbox)

    img_cnv.rectangle(bbox, fill="#000000")

    img_cnv.text((int(img_past.width + distance),
                  int(img_past.height + distance)),
                 footnote,
                 font=font_footnote,
                 fill=stroke_color,
                 stroke_fill="#000000",
                 anchor="rt"
                 )
    img_cnv.text((img.width // 2,
                  img_past.height + 2 * distance),
                 upper_text,
                 font=font_upper,
                 fill=upper_color,
                 anchor="mt"
                 )
    img_cnv.text((img.width // 2,
                  int(img_past.height + 2.25 * distance + 0.68 * text_size)),
                 bottom_text,
                 font=font_bottom,
                 fill=bottom_color,
                 anchor="mt"
                 )

    img.save(save_path)
    return save_path


def create_book(path: str,
                author: str,
                title: str,
                descriptor: str,
                annotation_location: str,
                annotation: list,
                author_backing_color: str,
                title_backing_color: str,
                logo_backing_color: str,
                size: int,
                distance: int) -> str:
    save_path = f'{path[:-4]}-mem-book.png'
    basic_color = "#faef9f"
    relation = 930 / 600
    illustration_height = int(size * relation * 370 / 930)

    small_distance = distance // 8
    descriptor_line_width = 2 * distance // 3

    img_past = Image.open(path).convert('RGB')
    img_logo = Image.open(f'{os.path.dirname(__file__)}/assets/logo.png').convert('RGBA')

    myriad_pro_bold = f'{os.path.dirname(__file__)}/assets/Myriad Pro Bold.OTF'
    myriad_pro_cond_bold = f'{os.path.dirname(__file__)}/assets/Myriad Pro Cond Bold.OTF'
    myriad_pro_cond_italic = f'{os.path.dirname(__file__)}/assets/Myriad Pro Cond Italic.OTF'

    img = Image.new('RGB', (size, int(size * relation)), color=basic_color)
    img_cnv = ImageDraw.Draw(img)

    img_cnv.rectangle((distance,
                       distance - 2 * small_distance,
                       size - distance,
                       distance - small_distance),
                      fill="#000000")

    img_cnv.rectangle((distance,
                       img.height - (distance - 2 * small_distance) - descriptor_line_width,
                       img.width - distance,
                       img.height - (distance - 2 * small_distance)),
                      fill="#000000")

    annotation_size = 120
    font_annotation = ImageFont.truetype(myriad_pro_cond_italic, 19)

    if annotation_location == 'l':
        position_annotation = int(1.5 * distance)
        position_l_title = int(2 * distance) + 153
        position_r_title = img.width - distance
    else:
        position_annotation = img.width - int(1.5 * distance) - 153
        position_l_title = distance
        position_r_title = img.width - int(2 * distance) - 153

    img_cnv.rectangle((position_l_title,
                       img.height - (distance - small_distance) - descriptor_line_width - annotation_size,
                       position_r_title,
                       img.height - (distance - small_distance) - descriptor_line_width),
                      fill=author_backing_color)

    img_cnv.text((position_annotation,
                  img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2) - 22),
                 annotation[0],
                 font=font_annotation,
                 fill='#000000',
                 anchor="lm"
                 )
    img_cnv.text((position_annotation,
                  img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2)),
                 annotation[1],
                 font=font_annotation,
                 fill='#000000',
                 anchor="lm"
                 )
    img_cnv.text((position_annotation,
                  img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2) + 22),
                 annotation[2],
                 font=font_annotation,
                 fill='#000000',
                 anchor="lm"
                 )

    if len(title) < 6:
        title_name_font = myriad_pro_bold
    else:
        title_name_font = myriad_pro_cond_italic

    if len(title) > 16:
        bottom_title = " ".join(title.split()[(len(title.split()) // 2 + 1):])
        upper_title = " ".join(title.split()[:(len(title.split()) - len(title.split()) // 2)])

        if len(upper_title) >= len(bottom_title):
            max_title = upper_title
        else:
            max_title = bottom_title

        title_size = size // 2
        title_font = ImageFont.truetype(title_name_font, title_size)
        title_width = img_cnv.textlength(max_title, font=title_font)

        while (title_width >= img.width - 3.5 * distance - 153) and \
                (title_size != 1):
            title_size = title_size - 1 if title_size - 1 > 0 else 1
            title_font = ImageFont.truetype(title_name_font, title_size)
            title_width = img_cnv.textlength(max_title, font=title_font)

        img_cnv.text((position_l_title + distance // 4,
                      img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2) - 5),
                     upper_title,
                     font=title_font,
                     fill='#000000',
                     anchor="lb"
                     )

        img_cnv.text((position_l_title + distance // 4,
                      img.height - (distance - small_distance) - descriptor_line_width - (annotation_size // 2) + 5),
                     bottom_title,
                     font=title_font,
                     fill='#000000',
                     anchor="lt"
                     )

    else:
        title_size = size // 2
        title_font = ImageFont.truetype(title_name_font, title_size)
        title_width = img_cnv.textlength(title, font=title_font)

        while (title_width >= img.width - 3.5 * distance - 153) and \
                (title_size != 1):
            title_size = title_size - 1 if title_size - 1 > 0 else 1
            title_font = ImageFont.truetype(title_name_font, title_size)
            title_width = img_cnv.textlength(title, font=title_font)

        if len(title) < 6:
            position = img.height - (distance - small_distance) - descriptor_line_width - int(0.82 * annotation_size // 2)
        else:
            position = img.height - (distance - small_distance) - descriptor_line_width - int(0.92 * annotation_size // 2)

        img_cnv.text((position_l_title + distance // 4,
                      position),
                     title,
                     font=title_font,
                     fill='#000000',
                     anchor="lm"
                     )

    if len(author.split()) == 1:
        bottom_author = author
        upper_author = "ХУЙ СЕРГЕЕВИЧ"
    else:
        bottom_author = author.split()[-1]
        upper_author = " ".join(author.split()[:-1])

    if len(upper_author.split()) == 2:
        upper_author_name_font = myriad_pro_cond_bold
    else:
        upper_author_name_font = myriad_pro_bold

    upper_author_size = size // 2
    upper_author_font = ImageFont.truetype(upper_author_name_font, upper_author_size)
    upper_author_width = img_cnv.textlength(upper_author, font=upper_author_font)

    while (upper_author_width >= (img.width - 2 * distance) - upper_author_size) and \
            (upper_author_size != 1):
        upper_author_size = upper_author_size - 1 if upper_author_size - 1 > 0 else 1
        upper_author_font = ImageFont.truetype(upper_author_name_font, upper_author_size)
        upper_author_width = img_cnv.textlength(upper_author, font=upper_author_font)

    bottom_author_size = size // 2
    bottom_author_font = ImageFont.truetype(myriad_pro_cond_bold, bottom_author_size)
    bottom_author_width = img_cnv.textlength(bottom_author, font=bottom_author_font)

    while (bottom_author_width >= (img.width - 2.5 * distance)) and \
            (bottom_author_size != 1):
        bottom_author_size = bottom_author_size - 1 if bottom_author_size - 1 > 0 else 1
        bottom_author_font = ImageFont.truetype(myriad_pro_cond_bold, bottom_author_size)
        bottom_author_width = img_cnv.textlength(bottom_author, font=bottom_author_font)

    # TODO
    #  Тут сложная логика через левую коленку, но если в двух словах
    #  скрипт вычислил свержу абсолютные значения для картинки, верхней и нижней имени автора.
    #  код ниже растягивает эти значения на оставшуюся часть картинки
    #
    #                    Срезаем место сверху
    #                    |          Срезаем место снизу
    #                    L_______   L_________________________________________________
    place = img.height - distance - distance - descriptor_line_width - annotation_size - (4 * small_distance)

    relation4place = place / (illustration_height + upper_author_size + bottom_author_size)

    illustration_height = int(illustration_height * relation4place)
    upper_author_size = int(upper_author_size * relation4place)
    bottom_author_size = int(bottom_author_size * relation4place)

    img_past = img_past.resize((size - (distance * 2), illustration_height))
    img.paste(img_past, (distance, distance))

    img_cnv.rectangle((distance,
                       distance + img_past.height + small_distance,
                       size - distance,
                       distance + img_past.height + 2 * small_distance),
                      fill="#000000")

    font_descriptor = ImageFont.truetype(myriad_pro_bold, 18)
    for i in range(len(f'+{descriptor}')):
        img_cnv.text((distance + int(img_past.width * (i / len(f'+{descriptor}'))),
                      img.height - (distance - 2 * small_distance) - descriptor_line_width // 2),
                     f' {descriptor}'[i],
                     font=font_descriptor,
                     fill=basic_color,
                     anchor="mm"
                     )

    # Чтобы было удобно считать, определяем новый «нуль» (Относительно низа картинки)
    zero_below_img = distance + img_past.height + 3 * small_distance

    img_cnv.rectangle((distance,
                       zero_below_img,
                       size - distance,
                       zero_below_img + upper_author_size),
                      fill=author_backing_color)

    img_cnv.rectangle((distance,
                       zero_below_img,
                       distance + upper_author_size,
                       zero_below_img + upper_author_size),
                      fill=logo_backing_color)

    img_logo = img_logo.resize((upper_author_size, upper_author_size))
    img.paste(img_logo,
              (distance,
               zero_below_img),
              mask=img_logo)

    img_cnv.text(((img.width + upper_author_size) // 2,
                  int(zero_below_img + 0.62 * upper_author_size)),
                 upper_author,
                 font=upper_author_font,
                 fill='#000000',
                 anchor="mm"
                 )

    img_cnv.rectangle((distance,
                       zero_below_img + small_distance + upper_author_size,
                       size - distance,
                       int(zero_below_img + small_distance + upper_author_size + bottom_author_size)),
                      fill=title_backing_color)

    img_cnv.text((img.width // 2,
                  int(zero_below_img + small_distance + upper_author_size + 0.62 * bottom_author_size)),
                 bottom_author,
                 font=bottom_author_font,
                 fill=basic_color,
                 anchor="mm"
                 )

    img.save(save_path)
    return save_path
