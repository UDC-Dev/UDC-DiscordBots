import discord
from discord.ext import commands
import os
import datetime
import asyncio

TOKEN = os.getenv("TOKEN")
intent = discord.Intents.default()
intent.message_content= True

client = commands.Bot(
    command_prefix='!',
    intents=intent
)

channel_id = int(os.environ.get("CHANNEL_ID"))
test_channel_id = int(os.environ.get("TEST_CHANNEL_ID"))

@client.command()
async def test(ctx):
    if ctx.channel.id == channel_id or ctx.channel.id == test_channel_id:
        await ctx.send("Announcement Bot is Working!")

@client.event
async def on_ready():
    print("Bot is ready!")

client.run(TOKEN)
