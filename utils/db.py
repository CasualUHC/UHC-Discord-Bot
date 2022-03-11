import json

import discord
from mojang import MojangAPI
from pymongo import MongoClient

from utils import embeds, config
from utils.skins import get_head


def format_name(name):
    if name.startswith('_'):
        return f'\\{name}'
    else:
        return name


class TeamsDB(object):
    def __init__(self):
        self.uri = config.mongo_uri
        self.client = MongoClient(self.uri)
        self.db = (self.client['UHC'])['teams']

    # --------------------
    def win_scoreboard(self):
        return embeds.wins(
            win_list=[f'{result["name"]}: {result["wins"]}' for result in self.db.find({}).sort("wins", -1)]
        )

    # --------------------

    def add_team(self, prefix: str, name: str, logo: str, colour: str, discord_colour: str):
        self.db.insert_one(
            {
                "_id": self.db.count(),
                "prefix": prefix,
                "name": name,
                "members": "",
                "logo": logo,
                "wins": 0,
                "colour": colour,
                "discord_colour": discord_colour
            }
        )
        return self.info(name)

    # --------------------

    def check_teams_for_player(self, player: str) -> str:

        for server in self.db.find({}):
            if player in server['members']:
                return server['name']

    # --------------------

    def get_wins(self, server: str) -> int:
        results = self.db.find({'name': server})

        for result in results:
            return result['wins']

    # --------------------

    def get_team(self, server: str) -> list:
        results = self.db.find({'name': server})

        for result in results:
            team = [f'\\{player}' if player.startswith('_') else player for player in result['members'].split(':')]
            if '' in team:
                team.clear()
                return team
            else:
                return team

    # --------------------

    def get_logo(self, server: str) -> str:
        results = self.db.find({'name': server})

        for result in results:
            return result['logo']

    # --------------------

    def get_colour(self, server: str) -> int:
        results = self.db.find({'name': server})

        for result in results:
            return int(f'0x{result["discord_colour"]}', 16)

    # --------------------

    def add_player(self, server: str, player: str):
        team = self.get_team(server)
        if self.check_teams_for_player(player):
            return embeds.player_already_on_team(
                player=player,
                server=self.check_teams_for_player(player),
                team=self.get_team(self.check_teams_for_player(player)),
                logo=self.get_logo(self.check_teams_for_player(player)),
                colour=self.get_colour(self.check_teams_for_player(player)))
        else:
            if len(team) > 4:
                return embeds.full_team(server, team, self.get_logo(server), self.get_colour(server))
            else:
                if player in team:
                    return embeds.player_already_on_team(
                        player=player,
                        server=server,
                        team=team,
                        logo=self.get_logo(server),
                        colour=self.get_colour(server)
                    )
                else:
                    team.append(player)
                    self.db.update_one({'name': server}, {'$set': {'members': ':'.join(team)}})
                    return embeds.add_player_success(
                        player=player,
                        server=server,
                        team=team,
                        head=get_head(player),
                        colour=self.get_colour(server)
                    )

    # --------------------

    def remove_player(self, server: str, player: str):
        team = self.get_team(server)
        if player not in team:
            return embeds.player_not_on_team(
                player=player,
                server=server,
                team=team,
                logo=self.get_logo(server),
                colour=self.get_colour(server)
            )
        else:
            team.remove(player)
            self.db.update_one({'name': server}, {'$set': {'members': ':'.join(team)}})
            return embeds.remove_player_success(
                player,
                server,
                team,
                self.get_logo(server),
                self.get_colour(server)
            )

    # --------------------

    def clear(self, server: str):
        self.db.update_one({'name': server}, {'$set': {'members': []}})

    # --------------------

    def info(self, server: str):
        return embeds.team_info(
            server=server,
            team=self.get_team(server),
            logo=self.get_logo(server),
            colour=self.get_colour(server)
        )

    # --------------------

    def to_json(self):
        with open('../Teams.json', 'w') as f:
            f.write(json.dumps([document for document in self.db.find()], indent=2))

    # --------------------


class PlayersDB(object):
    def __init__(self):
        self.uri = config.mongo_uri
        self.client = MongoClient(self.uri)
        self.db = (self.client['UHC'])['total_player_stats']

    def get_kills(self, player: str) -> int:
        results = self.db.find({'name': player})

        for result in results:
            return result['kills']

    def get_all_stats(self, player: str) -> discord.Embed:
        username = MojangAPI.get_username(MojangAPI.get_uuid(player))
        results = self.db.find({'name': username})
        if results:
            for result in results:
                del result['_id'], result['name']
                return embeds.player_stats(name=username, stats=result)
            else:
                return embeds.stats_not_found(name=player)

    def get_scoreboard(self, stat: str) -> discord.Embed:
        return embeds.scoreboard(
            stat=stat,
            scores=[f'\\{result["name"]}\\: {result[stat]}' for result in self.db.find({}).sort(stat, -1)]
        )
