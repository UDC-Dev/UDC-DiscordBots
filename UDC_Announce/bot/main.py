import discord
from discord.ext import commands
import os
import datetime
import asyncio
from schedule import *

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

async def announce_tommorow():
    channel = client.get_channel(channel_id)
    await channel.send("@everyone\n明日は定例会です！")

async def announce_today():
    channel = client.get_channel(channel_id)
    await channel.send("@everyone\n今日は定例会です！")

async def check_task():
    test_channel = client.get_channel(test_channel_id)
    buf1=datetime.datetime.strptime(today[-1], "%Y-%m-%d").date()
    buf2=datetime.datetime.strptime(tommrow[-1], "%Y-%m-%d").date()
    if datetime.date.today()>buf1 or datetime.date.today()>buf2:
        await test_channel.send("日程を追加してください")

async def testannounce_morning():
    test_channel = client.get_channel(test_channel_id)
    await test_channel.send("定時連絡(朝)")
    await check_task()

async def testannounce_evening():
    test_channel = client.get_channel(test_channel_id)
    await test_channel.send("定時連絡(夜)")
    await check_task()

async def check_time():
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
            if str(datetime.date.today()) in today:
                await announce_today()
            await testannounce_morning()
        # Evening check at 6 PM
        now = datetime.datetime.now()
        next_evening = now.replace(hour=18, minute=0, second=0, microsecond=0)
        seconds_until = (next_evening - now).total_seconds()
        await asyncio.sleep(seconds_until)
        if str(datetime.date.today()) in tommrow:
            await announce_tommorow()
        await testannounce_evening()

@client.event
async def on_ready():
    print("Bot is ready!")
    await check_time()

client.run(TOKEN)
