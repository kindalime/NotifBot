import os
import discord
import asyncpraw as praw
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import guild_only

class RedditCog(commands.Cog):
    def __init__(self):
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_SECRET")
        user_agent = "NotifBot:v1.0 (by u/CobaltGray0)"
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

        self.running = False
        self.sub = None
        self.match = None

    @commands.command(name="ping")
    @guild_only()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command(name="notif")
    @guild_only()
    async def notif(self, ctx, sub: str, match: str):
        if self.running:
            await ctx.send("Notif bot already running!")
            return

        self.running = True
        self.sub = sub
        self.match = match

        subreddit = await self.reddit.subreddit(sub)
        async for submission in subreddit.stream.submissions():
            if self.running:
                if match in submission.selftext.lower():
                    await ctx.send(f"{ctx.author.mention}: new link found!\nwww.reddit.com{submission.permalink}")

    @commands.command(name="notif_shutdown")
    @guild_only()
    async def notif_shutdown(self, ctx):
        if not self.running:
            await ctx.send("Notif bot is not currently running!")
        else:
            self.running = False
            await ctx.send("Notif bot shutdown successfully.")

    @commands.command(name="notif_info")
    @guild_only()
    async def notif_info(self, ctx):
        if self.running:
            await ctx.send(f"Notif bot currently running. Sub:{self.sub} Match:{self.match}")
        else:
            await ctx.send("Notif bot not running!")
