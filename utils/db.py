import discord
from discord import Embed
from mojang import MojangAPI
from PIL.Image import Image
from pymongo import MongoClient

from utils import config, embeds, image
from utils.skins import get_head


def format_name(name):
    if name.startswith("_"):
        return f"\\{name}"
    else:
        return name


class TeamsDB(object):
    def __init__(self):
        self.uri = config.mongo_uri
        self.client = MongoClient(self.uri)
        self.db = (self.client["UHC"])["teams"]

    # --------------------
    def win_scoreboard(self):
        return embeds.wins(
            win_list=[
                f'{result["name"]}: {result["wins"]}'
                for result in self.db.find({}).sort("wins", -1)
            ]
        )

    # --------------------

    def add_team(self, prefix: str, name: str, logo: str, colour: str, guilds):
        self.db.insert_one(
            {
                "_id": self.db.estimated_document_count(),
                "prefix": prefix,
                "name": name,
                "members": [],
                "logo": logo,
                "wins": 0,
                "colour": colour,
            }
        )
        return self.info(name, guilds)

    # --------------------

    def check_teams_for_player(self, player: str) -> str:

        for server in self.db.find({}):
            if player in server["members"]:
                return server["name"]

    # --------------------

    def get_wins(self, server: str) -> int:
        results = self.db.find({"name": server})

        for result in results:
            return result["wins"]

    # --------------------

    def get_team(self, server: str, guilds) -> list[str]:
        results = self.db.find({"name": server})
        for result in results:
            return [
                f"\\{player}" if player.startswith("_") else player
                for player in result["members"]
            ]
        else:
            self.add_team(server, server, "", "WHITE", guilds)
            return []

    # --------------------

    def get_logo(self, server: str) -> str:
        results = self.db.find({"name": server})

        for result in results:
            return result["logo"]

    # --------------------

    def get_colour(self, server: str) -> int:
        results = self.db.find({"name": server})

        for result in results:
            return int(f'0x{result["discord_colour"]}', 16)

    # --------------------

    def add_player(self, server: str, player: str, guilds):
        current_player_team = self.check_teams_for_player(player)
        if current_player_team:
            return embeds.player_already_on_team(
                player=player,
                server=current_player_team,
                team=self.get_team(current_player_team, guilds),
                logo=self.get_logo(current_player_team),
                colour=guilds.get_role(config.teams.get(current_player_team)).color,
            )
        else:
            team = self.get_team(server, guilds)
            new_team_colour = guilds.get_role(config.teams.get(server)).color
            if len(team) > 4:
                return embeds.full_team(
                    server, team, self.get_logo(server), new_team_colour
                )
            else:
                if player in team:
                    return embeds.player_already_on_team(
                        player=player,
                        server=server,
                        team=team,
                        logo=self.get_logo(server),
                        colour=new_team_colour,
                    )
                else:
                    team.append(player)
                    self.db.update_one({"name": server}, {"$push": {"members": player}})
                    return embeds.add_player_success(
                        player=player,
                        server=server,
                        team=team,
                        head=get_head(player),
                        colour=new_team_colour,
                    )

    # --------------------

    def remove_player(self, server: str, player: str, guilds):
        team = self.get_team(server, guilds)
        server_colour = guilds.get_role(config.teams.get(server)).color
        if player not in team:
            return embeds.player_not_on_team(
                player=player,
                server=server,
                team=team,
                logo=self.get_logo(server),
                colour=server_colour,
            )
        else:
            team.remove(player)
            self.db.update_one({"name": server}, {"$pull": {"members": player}})
            return embeds.remove_player_success(
                player, server, team, self.get_logo(server), server_colour
            )

    # --------------------

    def clear(self, server: str):
        self.db.update_one({"name": server}, {"$set": {"members": []}})

    # --------------------

    def info(self, server: str, guilds):
        return embeds.team_info(
            server=server,
            team=self.get_team(server, guilds),
            logo=self.get_logo(server),
            colour=guilds.get_role(config.teams.get(server)).color,
        )

    # --------------------

    def to_json(self):
        pass
        # with open('../Teams.json', 'w') as f:
        #     f.write(json.dumps([document for document in self.db.find()], indent=2))

    # --------------------


class PlayersDB(object):
    def __init__(self):
        self.uri = config.mongo_uri
        self.client = MongoClient(self.uri)
        self.db = (self.client["UHC"])["total_player_stats"]

    def get_kills(self, player: str) -> int:
        results = self.db.find({"name": player})

        for result in results:
            return result["kills"]

    def get_all_stats(self, player: str) -> discord.Embed:
        username = MojangAPI.get_username(MojangAPI.get_uuid(player))
        results = self.db.find({"name": username})
        if results:
            for result in results:
                del result["_id"], result["name"]
                return embeds.player_stats(name=username, stats=result)
            else:
                return embeds.stats_not_found(name=player)

    def get_scoreboard(self, stat: str, show_all: bool) -> tuple[Embed, Image]:
        results = [
            res
            for res in self.db.find({}).sort(stat, -1).limit(0 if show_all else 10)
            if res[stat] > 0
        ]
        embed = embeds.scoreboard(stat=stat, img_name="scoreboard.png")
        img = image.scoreboard(stat=stat, scores=results, img_name="scoreboard.png")
        return embed, img
