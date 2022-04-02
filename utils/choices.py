from dataclasses import dataclass, field

from discord import AppCommandOptionType
from discord.app_commands import Argument, Choice

from utils import config


@dataclass(frozen=True, kw_only=True)
class Option:
    name: str
    type: AppCommandOptionType
    description: str
    choices: list[Choice] = field(default_factory=list)


poll_options = [
    Option(
        name="poll_title",
        type=AppCommandOptionType.string,
        description="The question to ask the user.",
    ),
    Option(
        name="poll_description",
        type=AppCommandOptionType.string,
        description="The description of the poll.",
    ),
    *[
        Option(
            name=f"option_{i}",
            type=AppCommandOptionType.string,
            description=f"Option {i} of the poll.",
        )
        for i in range(1, 7)
    ],
]

scoreboard_options = Option(
    name="stat",
    type=AppCommandOptionType.string,
    description="The stat to display.",
    choices=[
        Choice(name="damage taken", value="damage taken"),
        Choice(name="damage dealt", value="damage dealt"),
        Choice(name="deaths", value="deaths"),
        Choice(name="kills", value="kills"),
    ],
)

scoreboard_show_all = Option(
    name="show_all",
    type=AppCommandOptionType.string,
    description="Whether to show all players or not.",
    choices=[
        Choice(name="All", value="All")
    ],
)

server_prefix = Option(
    name="prefix",
    type=AppCommandOptionType.string,
    description="The new prefix for the server.",
)

server_name = Option(
    name="name",
    type=AppCommandOptionType.string,
    description="The new name for the server.",
)

server_logo = Option(
    name="logo",
    type=AppCommandOptionType.string,
    description="The new logo for the server.",
)

server_colour = Option(
    name="colour",
    type=AppCommandOptionType.string,
    description="The new colour for the server.",
    choices=[
        Choice(name="Dark Red", value="dark_red"),
        Choice(name="red", value="red"),
        Choice(name="Gold", value="gold"),
        Choice(name="Yellow", value="yellow"),
        Choice(name="Dark Green", value="dark_green"),
        Choice(name="Green", value="green"),
        Choice(name="Aqua", value="aqua"),
        Choice(name="Dark Aqua", value="dark_aqua"),
        Choice(name="Dark Blue", value="dark_blue"),
        Choice(name="Blue", value="blue"),
        Choice(name="Light Purple", value="light_purple"),
        Choice(name="Dark Purple", value="dark_purple"),
        Choice(name="White", value="white"),
        Choice(name="Gray", value="gray"),
        Choice(name="Dark Gray", value="dark_gray"),
        Choice(name="Black", value="black"),
    ],
)

server_discord_colour = Option(
    name="discord_colour",
    type=AppCommandOptionType.string,
    description="The new discord colour for the server.",
)

servers = Option(
    name="server",
    type=AppCommandOptionType.string,
    description="The server to display.",
    choices=[Choice(name=team, value=team) for team in config.teams],
)

player_ign = Option(
    name="ign",
    type=AppCommandOptionType.string,
    description="The player's ign.",
)
