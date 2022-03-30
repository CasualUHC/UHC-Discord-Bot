import websockets
import websockets.exceptions
from discord.ext import commands


class Websocket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def main(self, websocket):
        chat_link = self.bot.get_channel(0)
        try:
            while True:
                message = await websocket.recv()
                await chat_link.send(message)
        except websockets.exceptions.ConnectionClosed:
            await chat_link.send("Connection to server has been lost")


def setup(bot):
    bot.add_cog(Websocket(bot))
