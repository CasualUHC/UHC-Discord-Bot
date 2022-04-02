import json

import discord
from discord.abc import Snowflake

colour = 0xFF66FF
prefix = "!"
admins = []
teams = {}
mongo_uri = ""
discord_token = ""
guilds: list[Snowflake] = []
embeds = {}


def initialise() -> None:
    global admins, teams, mongo_uri, discord_token, guilds, embeds

    with open("Roles.json") as file:
        config = json.loads(file.read())
        admins = config["admins"]
        teams = config["teams"]

    with open("Config.json") as file:
        config = json.loads(file.read())
        mongo_uri = config["mongo"]
        discord_token = config["discord"]
        guilds = [discord.Object(guild_id) for guild_id in config["guilds"]]

    with open("Embeds.json") as file:
        embeds = json.loads(file.read())
