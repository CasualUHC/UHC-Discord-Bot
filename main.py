import pathlib

import discord
import websockets
from discord.ext import commands
from discord_slash import SlashCommand

from utils import config

intents = discord.Intents.all()


class UHCBot(commands.Bot):
    async def start(self, *args, **kwargs):
        async def callback(websocket):
            cog = self.get_cog('Websocket')
            if not cog:
                print('websocket cog not found')
                return
            return await cog.main(websocket)

        async with websockets.serve(callback, 'localhost', 12345):
            return await super().start(*args, **kwargs)


bot = UHCBot(
    command_prefix='!',
    help_command=None,
    intents=intents
)

slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print('UHC bot is online')


def initialise() -> None:
    config.initialise()

    for path in pathlib.Path('./cogs').glob('*.py'):
        bot.load_extension(f'cogs.{path.stem}')

    bot.run(config.discord_token)


if __name__ == '__main__':
    initialise()
