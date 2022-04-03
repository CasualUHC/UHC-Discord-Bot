import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from mojang import MojangAPI

from main import client
from utils import choices, config, db, decorators
from utils.config import admins


class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = db.TeamsDB()

    @commands.command(name="wins")
    async def _wins(self, ctx: Context):
        await ctx.send(embed=self.db.win_scoreboard())

    @client.command(
        name="addTeam", description="Add a team to the database", guilds=config.guilds
    )
    @app_commands.checks.has_any_role(*admins)
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

    @app_commands.command(name="addplayer", description="Add a player to a team")
    @app_commands.checks.has_any_role("Administrator")
    @decorators.params_wrapper([choices.servers, choices.player_ign])
    async def add_player(self, interaction: discord.Interaction, server: str, ign: str):
        username = MojangAPI.get_username(MojangAPI.get_uuid(ign))
        if username:
            await interaction.response.send_message(
                embed=self.db.add_player(server, username, interaction.guild)
            )
        else:
            await interaction.response.send_message.send(f"'{ign}' is not a valid IGN!")
        self.db.to_json()

    @app_commands.command(
        name="removeplayer", description="Remove a player from a team"
    )
    @decorators.params_wrapper([choices.servers, choices.player_ign])
    @decorators.belongs_to_same_team()
    async def remove_player(
        self, interaction: discord.Interaction, server: str, ign: str
    ):
        username = MojangAPI.get_username(MojangAPI.get_uuid(ign))
        if username:
            await interaction.response.send_message(
                embed=self.db.remove_player(server, username, interaction.guild)
            )
        else:
            await interaction.response.send_message(f"'{ign}' is not a valid IGN")
        self.db.to_json()

    @app_commands.command(name="teaminfo", description="Get team info")
    @decorators.params_wrapper([choices.servers])
    async def team_info(self, interaction: discord.Interaction, server: str):
        await interaction.response.send_message(
            embed=self.db.info(server, interaction.guild)
        )
        self.db.to_json()

    @app_commands.command(name="clearteam", description="Clear a team")
    @decorators.params_wrapper([choices.servers])
    async def clear(self, interaction: discord.Interaction, server: str):
        self.db.clear(server)
        await interaction.response.send_message(f"Successfully cleared {server}'s team")


async def setup(bot):
    await bot.add_cog(Teams(bot))
