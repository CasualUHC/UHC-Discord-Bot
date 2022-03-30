import datetime
from typing import Iterator

import discord
from PIL.Image import Image

from utils import config, skins

uhc_logo = "https://cdn.discordapp.com/attachments/775083888602513439/804920103850344478/UHC_icon.png"

letter_emojis = [
    "🇦",
    "🇧",
    "🇨",
    "🇩",
    "🇪",
    "🇫",
    "🇬",
    "🇭",
    "🇮",
    "🇯",
    "🇰",
    "🇱",
    "🇲",
    "🇳",
    "🇴",
    "🇵",
    "🇶",
    "🇷",
    "🇸",
    "🇹",
]


# --------------------


def poll(title: str, description: str, options: list) -> discord.Embed:
    options = [f"{letter_emojis[i]} {options[i]}" for i in range(len(options))]
    embed = discord.Embed(
        title=title.title(),
        description=f"{description.title()}\n\n" + "\n".join(options),
        color=config.colour,
    )
    embed.set_thumbnail(url=uhc_logo)
    return embed


# --------------------


def wins(win_list: list) -> discord.Embed:
    embed = discord.Embed(
        title="Wins", description="\n".join(win_list), colour=config.colour
    )
    embed.set_thumbnail(url=uhc_logo)
    return embed


# --------------------


def scoreboard(stat: str, img_name: str) -> discord.Embed:
    embed = discord.Embed.from_dict(
        {
            "title": f"{stat.capitalize()} Scoreboard",
            "color": 0x7ed6df,
            "image": {"url": f"attachment://{img_name}"},
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "footer": {"text": "UHC Scoreboard", "icon_url": uhc_logo},
        }
    )

    return embed


# --------------------


def stats_not_found(name: str) -> discord.Embed:
    embed = discord.Embed(
        title="Database Error",
        description=f'Player "{name}" does not have any statistics yet',
        colour=discord.Colour.red(),
    )
    return embed


# --------------------


def player_stats(name: str, stats: dict) -> discord.Embed:
    stats_list = [f"{key.title()}: {value}" for (key, value) in stats.items()]
    embed = discord.Embed(
        title=f"{name}", description="\n".join(stats_list), colour=config.colour
    )
    embed.set_thumbnail(url=skins.get_body(name))
    return embed


# --------------------


def team_info(server: str, team: list, logo: str, colour: int) -> discord.Embed:
    embed = discord.Embed(
        title=f"Info for {server}",
        colour=colour,
        description="**Current Team**\n" + "\n".join(team),
    )
    embed.set_thumbnail(url=logo)
    return embed


# --------------------


def add_player_success(
    player: str, server: str, team: list, head: str, colour: int
) -> discord.Embed:
    embed = discord.Embed(
        title=f"Added {player} to {server}'s team",
        colour=colour,
        description="**Current Team**\n" + "\n".join(team),
    )
    embed.set_thumbnail(url=head)
    return embed


# --------------------


def full_team(server: str, team: list, logo: str, colour: int) -> discord.Embed:
    embed = discord.Embed(
        title=f"{server}'s team is full",
        colour=colour,
        description="**Current Team**\n" + "\n".join(team),
    )
    embed.set_thumbnail(url=logo)
    return embed


# --------------------


def player_already_on_team(
    player: str, server: str, team: list, logo: str, colour: int
) -> discord.Embed:
    embed = discord.Embed(
        title=f"{player} is already on {server}'s team",
        colour=colour,
        description="**Current Team**\n" + "\n".join(team),
    )
    embed.set_thumbnail(url=logo)
    return embed


# --------------------


def player_not_on_team(
    player: str, server: str, team: list, logo: str, colour: int
) -> discord.Embed:
    embed = discord.Embed(
        title=f"{player} is not on {server}'s team",
        colour=colour,
        description="**Current Team**\n" + "\n".join(team),
    )
    embed.set_thumbnail(url=logo)
    return embed


# --------------------


def remove_player_success(
    player: str, server: str, team: list, logo: str, colour: int
) -> discord.Embed:
    embed = discord.Embed(
        title=f"Successfully removed {player} from {server}'s team",
        colour=colour,
        description="**Current Team**\n" + "\n".join(team),
    )
    embed.set_thumbnail(url=logo)
    return embed


# --------------------


def faq() -> list[discord.Embed]:
    faq_config: dict = config.embeds["faq"]

    embeds = []

    embed = discord.Embed(title="UHC INFO", color=faq_config["colour"])

    faq_config = faq_config.copy()
    faq_field = faq_config.pop("FAQ")

    for field in faq_config:
        group = faq_config[field]
        if type(group) == list:
            embed.add_field(name=field, value=" ".join(faq_config[field]), inline=True)

    embeds.append(embed)

    embed = discord.Embed(
        title="UHC FAQ", color=faq_config["colour"], description=" ".join(faq_field)
    )

    embeds.append(embed)

    return embeds


def rules() -> discord.Embed:
    rules_config = config.embeds["rules"]

    embed = discord.Embed(
        title="UHC Rules!",
        color=rules_config["colour"],
        description=" ".join(rules_config["Description"]),
    )
    return embed
