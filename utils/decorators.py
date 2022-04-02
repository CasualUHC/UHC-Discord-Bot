import discord
from discord import app_commands

from utils import config
from utils.choices import Option


def add_config_guilds():
    def wrapper(func):
        app_commands.guilds(*config.guilds)(func)
        return func

    return wrapper


def belongs_to_same_team():
    def predicate(interaction: discord.Interaction, **kwargs):
        return (
            app_commands.checks.has_any_role("Administrator")(interaction)
            or interaction.guild.get_role(config.teams.get(kwargs["server"]))
            in interaction.user.roles
        )

    return app_commands.check(predicate=predicate)


def params_wrapper(arguments: list[Option]):
    def wrapper(func):
        add_config_guilds()(func)
        func.__discord_app_commands_param_description__ = {}
        func.__discord_app_commands_param_choices__ = {}

        for argument in arguments:
            func.__discord_app_commands_param_choices__[
                argument.name
            ] = argument.choices
            func.__discord_app_commands_param_description__[
                argument.name
            ] = argument.description
        return func

    return wrapper
