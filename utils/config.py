import json

colour = 0xff66ff
admins = []
teams = {}
mongo_uri = ""
discord_token = ""
guilds = []
embeds = {}


def initialise() -> None:
    global admins, teams, mongo_uri, discord_token, guilds, embeds

    with open("RolesTemplate.json") as file:
        config = json.loads(file.read())
        admins = config["admins"]
        teams = config["teams"]

    with open("ConfigTemplate.json") as file:
        config = json.loads(file.read())
        mongo_uri = config["mongo"]
        discord_token = config["discord"]
        guilds = config["guilds"]

    with open("EmbedsTemplate.json") as file:
        embeds = json.loads(file.read())
