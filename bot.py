import os
import random
import discord
import json
from dotenv import load_dotenv
from discord.ext import commands
from cog import RedditCog

class NotifBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="?")
        load_dotenv()
        self.token = os.getenv('DISCORD_TOKEN')
        self.reddit = RedditCog()
        self.add_cog(self.reddit)

    async def on_ready(self):
        serv = os.getenv('DISCORD_SERVER')
        server = discord.utils.get(self.guilds, name=serv)

    async def on_error(self, event, *args, **kwargs):
        """Simple error function that logs errors and raises all but unhandled messages."""

        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                f.write(f'Error: {args[0]}\n')
                raise

    def run(self):
        super().run(self.token)

if __name__ == "__main__":
    bot = NotifBot()
    bot.run()
