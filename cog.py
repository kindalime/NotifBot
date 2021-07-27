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

    @commands.command(name="ping")
    @guild_only()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command(name="notif")
    @guild_only()
    async def notif(self, ctx, sub: str, match: str):
        subreddit = await self.reddit.subreddit(sub)
        async for submission in subreddit.stream.submissions():
            if match in submission.selftext:
               await ctx.send(f"{ctx.author.mention}: new link found!\n{submission.permalink}")
