import asyncio

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext

from utils import config, embeds, slash
from utils.db import PlayersDB, TeamsDB


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = TeamsDB()

    @commands.command(name="json")
    @commands.has_any_role("Devs", "Administrator")
    async def _json(self, ctx):
        self.db.to_json()
        await ctx.send(file=discord.File("Teams.json"))

    @commands.command(name="faq")
    @commands.has_any_role("Devs", "Administrator")
    async def faq(self, ctx: SlashContext):
        faq_embeds = embeds.faq()
        for embed in faq_embeds:
            await ctx.send(embed=embed)

    @commands.command(name="rules")
    @commands.has_any_role("Devs", "Administrator")
    async def rules(self, ctx):
        await ctx.send(embed=embeds.rules())

    @commands.command(name="all_stats")
    @commands.has_any_role("Devs", "Administrator")
    async def all_stats(self, ctx):
        database = PlayersDB()
        player_list = [result["name"] for result in database.db.find({})]
        for player in player_list:
            await ctx.send(embed=database.get_all_stats(player=player))

    @commands.command(name="reload")
    @commands.has_any_role("Devs", "Administrator")
    async def reload(self, ctx):
        config.initialise()
        await ctx.send("Reloaded Config!")

    @cog_ext.cog_slash(
        name="shutdown",
        description="Gracefully shutdown the bot",
        permissions={
            config.guilds[0]: [
                {"id": 800222768775823380, "type": 1, "permission": True}  # dev role
            ]
        },
        guild_ids=config.guilds,
    )
    async def shutdown(self, ctx):
        await ctx.send("Shutting Down...")
        await self.bot.close()

    @cog_ext.cog_slash(
        name="poll",
        guild_ids=config.guilds,
        description="create a poll",
        options=slash.poll_options,
    )
    # probably a better way to do this, but I'm too damn tired to figure out kwargs bullshit right now
    async def _poll(
        self, ctx: SlashContext, poll_title: str, poll_description: str, **args
    ):
        options = [option for option in args.values() if option]

        msg = await ctx.send(
            embed=embeds.poll(
                title=poll_title, description=poll_description, options=options
            )
        )
        for i in range(len(options)):
            await msg.add_reaction(embeds.letter_emojis[i])


def setup(bot):
    bot.add_cog(Admin(bot))
