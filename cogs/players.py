from discord.ext import commands
from discord_slash import cog_ext

from utils.db import PlayersDB
from utils import slash, config


class Players(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = PlayersDB()

    @cog_ext.cog_slash(
        name='stats',
        guild_ids=config.guilds,
        options=[
            slash.ign
        ]
    )
    async def stats(self, ctx, ign: str):
        await ctx.send(embed=self.db.get_all_stats(player=ign))

    @cog_ext.cog_slash(
        name='scoreboard',
        guild_ids=config.guilds,
        options=[
            slash.scoreboard_options
        ]
    )
    async def scoreboard(self, ctx, stat):
        await ctx.send(embed=self.db.get_scoreboard(stat=stat))


def setup(bot):
    bot.add_cog(Players(bot))
