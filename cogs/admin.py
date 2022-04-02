import discord
from discord import app_commands
from discord.ext import commands

from utils import choices, config, db, decorators, embeds


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = db.TeamsDB()

    @commands.command(name="json")
    @commands.has_any_role("Devs", "Administrator")
    async def _json(self, ctx: commands.Context):
        self.db.to_json()
        await ctx.send(file=discord.File("Teams.json"))

    @commands.command(name="faq")
    @commands.has_any_role("Devs", "Administrator")
    async def faq(self, ctx: commands.Context):
        faq_embeds = embeds.faq()
        for embed in faq_embeds:
            await ctx.send(embed=embed)

    @commands.command(name="rules")
    @commands.has_any_role("Devs", "Administrator")
    async def rules(self, ctx: commands.Context):
        await ctx.send(embed=embeds.rules())

    @commands.command(name="all_stats")
    @commands.has_any_role("Devs", "Administrator")
    async def all_stats(self, ctx: commands.Context):
        database = db.PlayersDB()
        player_list = [result["name"] for result in database.db.find({})]
        for player in player_list:
            await ctx.send(embed=database.get_all_stats(player=player))

    @commands.command(name="reload")
    @commands.has_any_role("Devs", "Administrator")
    async def reload(self, ctx: commands.Context):
        config.initialise()
        await ctx.send("Reloaded Config!")

    @app_commands.command(
        name="shutdown",
        description="Gracefully shutdown the bot",
    )
    @decorators.add_config_guilds()
    @app_commands.checks.has_any_role("Devs", "Administrator")
    async def shutdown(self, ctx: commands.Context):
        await ctx.send("Shutting Down...")
        await self.bot.close()

    @app_commands.command(name="poll", description="Create a poll")
    @decorators.params_wrapper(choices.poll_options)
    async def _poll(
        self,
        interaction: discord.Interaction,
        poll_title: str,
        poll_description: str,
        option_1: str,
        option_2: str,
        option_3: str = None,
        option_4: str = None,
        option_5: str = None,
        option_6: str = None,
    ):
        options = list(
            filter(
                lambda o: o is not None,
                [option_1, option_2, option_3, option_4, option_5, option_6],
            )
        )
        await interaction.response.send_message(
            embed=embeds.poll(
                title=poll_title, description=poll_description, options=options
            )
        )
        response = await interaction.original_message()
        for i in range(len(options)):
            await response.add_reaction(embeds.letter_emojis[i])


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
