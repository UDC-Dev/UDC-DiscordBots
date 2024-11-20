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

@client.command()
async def test(ctx):
    if ctx.channel.id == channel_id or ctx.channel.id == test_channel_id:
        await ctx.send("Announcement Bot is Working!")

async def announce_tommorow():
    channel = client.get_channel(channel_id)
    await channel.send("@everyone\n明日は定例会です！")

async def announce_today():
    channel = client.get_channel(channel_id)
    await channel.send("@everyone\n今日は定例会です！")

async def testannounce_morning(day_of_week):
    test_channel = client.get_channel(test_channel_id)
    await test_channel.send(f"定時連絡(朝) {day_of_week}")

async def testannounce_evening(day_of_week):
    test_channel = client.get_channel(test_channel_id)
    await test_channel.send(f"定時連絡(夜) {day_of_week}")

async def check_time():
    plus=7 #起動時に決める(0/7)
    while True:
        # Morning check at 6 AM
        now = datetime.datetime.now()
        next_morning = now.replace(hour=6, minute=0, second=0, microsecond=0)
        if 6<=now.hour<18:
            pass
        else:
            if 18<=now.hour<=23:
                next_morning += datetime.timedelta(days=1)
            seconds_until = (next_morning - now).total_seconds()
            await asyncio.sleep(seconds_until)
            current_time = datetime.datetime.now()
            day_of_week = (current_time.weekday()+plus)
            if today[day_of_week] == 1:
                await announce_today()
            await testannounce_morning(day_of_week)
        # Evening check at 6 PM
        now = datetime.datetime.now()
        next_evening = now.replace(hour=18, minute=0, second=0, microsecond=0)
        seconds_until = (next_evening - now).total_seconds()
        await asyncio.sleep(seconds_until)
        current_time = datetime.datetime.now()
        day_of_week = (current_time.weekday()+plus)
        if tommorow[day_of_week] == 1:
            await announce_tommorow()
        await testannounce_evening(day_of_week)
        if day_of_week==13:
            plus=0
        elif day_of_week==6:
            plus=7

@client.event
async def on_ready():
    print("Bot is ready!")
    await check_time()

client.run(TOKEN)
