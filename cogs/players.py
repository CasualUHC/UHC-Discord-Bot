import discord
from discord import app_commands
from discord.ext import commands

from utils import choices, db, decorators, image


class Players(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = db.PlayersDB()

    @app_commands.command(name="stats", description="Shows your stats.")
    @decorators.params_wrapper([choices.player_ign])
    async def stats(self, interaction: discord.Interaction, ign: str):
        (embed, scoreboard) = self.db.get_stat_image(player=ign)
        if scoreboard is None:
            scoreboard = discord.utils.MISSING
        await interaction.response.send_message(embed=embed, file=scoreboard)

    @app_commands.command(
        name="scoreboard",
        description="Shows the scoreboard for a given stat.",
    )
    @decorators.params_wrapper(
        [choices.scoreboard_options, choices.scoreboard_show_all]
    )
    async def scoreboard(
        self, interaction: discord.Interaction, stat: str, show_all: str = None
    ):
        (embed, scoreboard) = self.db.get_scoreboard(
            stat=stat, show_all=(show_all == "all")
        )
        await interaction.response.send_message(embed=embed, file=scoreboard)


async def setup(bot):
    await bot.add_cog(Players(bot))
