import discord_slash
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_permission
from mojang import MojangAPI

from utils import config, slash
from utils.config import admins
from utils.db import TeamsDB


class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = TeamsDB()

    @commands.command(name="wins")
    async def _wins(self, ctx):
        await ctx.send(embed=self.db.win_scoreboard())

    @cog_ext.cog_slash(
        name="addTeam",
        guild_ids=config.guilds,
        options=[
            slash.server_prefix,
            slash.server_name,
            slash.server_logo,
            slash.server_colour,
        ],
        default_permission=False,
        permissions={
            config.guilds[0]: [
                create_permission(admins[0], SlashCommandPermissionType.ROLE, True),
            ]
        },
    )
    async def add_team(
        self, ctx, prefix: str, name: str, logo: str, server_colour: str
    ):
        await ctx.send(
            embed=self.db.add_team(
                prefix=prefix,
                name=name,
                logo=logo,
                colour=server_colour,
                guilds=self.bot.guilds,
            )
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

    @cog_ext.cog_slash(
        name="addPlayer", guild_ids=config.guilds, options=[slash.servers, slash.ign]
    )
    async def add_player(self, ctx: discord_slash.SlashContext, server: str, ign: str):
        if ctx.guild.get_role(admins[0]) not in ctx.author.roles:
            if ctx.guild.get_role(config.teams.get(server)) not in ctx.author.roles:
                await ctx.send(f"You do not have permission add players to {server}")
                return

        username = MojangAPI.get_username(MojangAPI.get_uuid(ign))

        if username:
            await ctx.send(embed=self.db.add_player(server, username, ctx.guild))
        else:
            await ctx.send(f"'{ign}' is not a valid IGN!")

        self.db.to_json()

    @cog_ext.cog_slash(
        name="removePlayer", guild_ids=config.guilds, options=[slash.servers, slash.ign]
    )
    async def remove_player(self, ctx, server: str, ign: str):
        if ctx.guild.get_role(admins[0]) not in ctx.author.roles:
            if ctx.guild.get_role(config.teams.get(server)) not in ctx.author.roles:
                await ctx.send(
                    f"You do not have permission remove players from {server}"
                )
                return

        username = MojangAPI.get_username(MojangAPI.get_uuid(ign))

        if username:
            await ctx.send(embed=self.db.remove_player(server, username, ctx.guild))
        else:
            await ctx.send(f"'{ign}' is not a valid IGN")

        self.db.to_json()

    @cog_ext.cog_slash(
        name="teamInfo", guild_ids=config.guilds, options=[slash.servers]
    )
    async def team_info(self, ctx, server: str):
        await ctx.send(embed=self.db.info(server, ctx.guild))

        self.db.to_json()

    @cog_ext.cog_slash(
        name="clearTeam",
        guild_ids=config.guilds,
        options=[
            slash.servers,
        ],
    )
    async def clear(self, ctx, server: str):
        self.db.clear(server)
        await ctx.send(f"Successfully cleared {server}'s team")


def setup(bot):
    bot.add_cog(Teams(bot))
