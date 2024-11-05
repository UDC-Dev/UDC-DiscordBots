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
#月曜が0,日曜が6
today =  [1,0,0,0,0,0,0,0,1,0,0,0,0,0]
tommorow=[0,0,0,0,0,0,0,1,0,0,0,0,0,1]
channel_id = int(os.environ.get("CHANNEL_ID"))
test_channel_id = int(os.environ.get("TEST_CHANNEL_ID"))
channel = client.get_channel(channel_id)
test_channel = client.get_channel(test_channel_id)
plus=7 #起動時に決める(0/7)

@client.command
async def test(ctx):
    if ctx.id == channel_id or ctx.id == test_channel_id:
        await ctx.send("Announcement Bot is Working!")

async def announce_tommorow():
    await channel.send("@everyone\n明日は定例会です！")

async def announce_today():
    await channel.send("@everyone\n今日は定例会です！")

async def testannounce_morning():
    await test_channel.send("定時連絡(朝)")

async def testannounce_evening():
    await test_channel.send("定時連絡(夜)")

async def check_time():
    while True:
        # Morning check at 6 AM
        now = datetime.datetime.now()
        next_morning = now.replace(hour=6, minute=0, second=0, microsecond=0)
        if now >= next_morning:
            next_morning += datetime.timedelta(days=1)
        seconds_until = (next_morning - now).total_seconds()
        await asyncio.sleep(seconds_until)
        current_time = datetime.datetime.now()
        day_of_week = (current_time.weekday()+plus)
        if today[day_of_week] == 1:
            await announce_today()
        await testannounce_morning()
        # Evening check at 6 PM
        now = datetime.datetime.now()
        next_evening = now.replace(hour=18, minute=0, second=0, microsecond=0)
        seconds_until = (next_evening - now).total_seconds()
        await asyncio.sleep(seconds_until)
        current_time = datetime.datetime.now()
        day_of_week = (current_time.weekday()+plus)
        if tommorow[day_of_week] == 1:
            await announce_tommorow()
        await testannounce_evening()

@client.event
async def on_ready():
    print("Bot is ready!")
    await check_time()

client.run(TOKEN)
