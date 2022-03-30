import io
import os
from operator import itemgetter

from discord import File
from PIL import Image, ImageDraw, ImageFont

MC_FONT = ImageFont.truetype(
    os.path.join(os.getcwd(), "assets", "minecraft.ttf"), size=20
)


def get_pixel_draw() -> ImageDraw.ImageDraw:
    return ImageDraw.Draw(Image.new("1", (1, 1)))


def scoreboard(stat: str, scores: list[dict], img_name: str) -> Image:
    draw = get_pixel_draw()

    header = stat.capitalize()
    header_size = draw.textsize(header, font=MC_FONT)
    spacing = 2
    padding = 5

    columns = {
        "name": "\n".join(score["name"] for score in scores),
        "values": "\n".join(str(score[stat]) for score in scores),
    }

    column_size = {
        k: draw.textsize(v, font=MC_FONT, spacing=spacing) for k, v in columns.items()
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
        font=MC_FONT,
        fill="#BFBFBF",
        spacing=spacing,
    )

    draw.text(
        xy=(padding * 2 + spacing + column_size["name"][0], header_size[1] + padding * 2),
        text=columns["values"],
        font=MC_FONT,
        fill="#FF5555",
        spacing=spacing,
        align="right",
    )

    draw.text(
        xy=((total_width - header_size[0]) / 2, padding),
        text=header,
        font=MC_FONT,
        fill="#5555FF",
        spacing=spacing,
    )

    with io.BytesIO() as buffer:
        image.save(buffer, "png")
        buffer.seek(0)
        scoreboard_image = File(fp=buffer, filename=img_name)

    return scoreboard_image
