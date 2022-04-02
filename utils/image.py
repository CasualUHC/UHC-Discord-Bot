import io
import os
from operator import itemgetter

import requests
from discord import File
from PIL import Image, ImageDraw, ImageFont

from utils import skins


def get_mc_font(size: int = 20) -> ImageFont:
    return ImageFont.truetype(
        os.path.join(os.getcwd(), "assets", "minecraft.ttf"), size=size
    )


def get_pixel_draw() -> ImageDraw.ImageDraw:
    return ImageDraw.Draw(Image.new("1", (1, 1)))


def scoreboard(stat: str, scores: list[dict], img_name: str) -> File:
    mc_font = get_mc_font()
    draw = get_pixel_draw()

    header = stat.capitalize()
    header_size = draw.textsize(header, font=mc_font)
    spacing = 2
    padding = 5

    columns = {
        "name": "\n".join(score["name"] for score in scores),
        "values": "\n".join(str(score[stat]) for score in scores),
    }

    column_size = {
        k: draw.textsize(v, font=mc_font, spacing=spacing) for k, v in columns.items()
    }

    total_width = (
            max(header_size[0], sum(size[0] for size in column_size.values())) + padding * 3
    )
    total_height = header_size[1] + column_size["name"][1] + padding * 3 + spacing

    image = Image.new("RGB", (total_width, total_height), color="#2c2f33")
    draw = ImageDraw.Draw(image)

    draw.text(
        xy=(padding + spacing, header_size[1] + padding * 2),
        text=columns["name"],
        font=mc_font,
        fill="#BFBFBF",
        spacing=spacing,
    )

    draw.text(
        xy=(
            padding * 2 + spacing + column_size["name"][0],
            header_size[1] + padding * 2,
        ),
        text=columns["values"],
        font=mc_font,
        fill="#FF5555",
        spacing=spacing,
        align="right",
    )

    draw.text(
        xy=((total_width - header_size[0]) / 2, padding),
        text=header,
        font=mc_font,
        fill="#5555FF",
        spacing=spacing,
    )

    with io.BytesIO() as buffer:
        image.save(buffer, "png")
        buffer.seek(0)
        scoreboard_image = File(fp=buffer, filename=img_name)

    return scoreboard_image


def player_stats(name: str, scores: dict, img_name: str) -> File | None:
    size_y = 384
    size_x = 384
    image = Image.new("RGBA", (size_x, size_y), color="#2c2f33FF")
    draw = ImageDraw.Draw(image)
    mc_font = get_mc_font(26)

    logical_order = [
        "Damage Dealt",
        "Damage Taken",
        "Kills",
        "Deaths",
    ]

    default_area = draw.textsize("MMMMMMMMMMMM", font=mc_font)

    diff_between_values = default_area[1] + 5
    diff_between_stats = default_area[1] + 24

    draw.text(
        xy=(10, 10),
        text=name,
        font=get_mc_font(48),
        fill="#5555FF",
    )

    stat_pos = (10, 88)
    for i, stat in enumerate(logical_order):
        draw.text(
            xy=stat_pos,
            text=stat + ":",
            font=mc_font,
            fill="#BFBFBF",
        )
        stat_pos = (stat_pos[0], stat_pos[1] + diff_between_values)
        draw.text(
            xy=stat_pos,
            text=str(scores[stat.lower()]),
            font=mc_font,
            fill="#FF5555",
        )
        stat_pos = (stat_pos[0], stat_pos[1] + diff_between_stats)

    with io.BytesIO() as buffer:
        size = 280
        r = requests.get(skins.get_body(name, size))
        if r.status_code == 200:
            buffer.write(r.content)
            buffer.seek(0)
            buff_image = Image.open(buffer)
            image.paste(buff_image, (size_x - int(size * 0.6171875) - 10, (size_y - size + 32) // 2), buff_image)
            buffer.seek(0)
            image.save(buffer, "png")
            buffer.seek(0)
            skin_image = File(fp=buffer, filename=img_name)
        else:
            return None

    return skin_image
