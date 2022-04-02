import asyncio
import pathlib

import discord
from discord.app_commands import CommandTree
from discord.ext.commands import Bot

from utils import config

client: Bot = Bot(command_prefix="!", help_command=None, intents=discord.Intents.all())
tree: CommandTree = client.tree


@client.event
async def on_ready() -> None:
    print("UHC bot is online")


@client.event
async def on_connect() -> None:
    for guild in config.guilds:
        await tree.sync(guild=guild)


async def load() -> None:
    config.initialise()

    for path in pathlib.Path("./cogs").glob("*.py"):
        await client.load_extension(f"cogs.{path.stem}")


if __name__ == "__main__":
    asyncio.run(load())
    client.run(config.discord_token)
