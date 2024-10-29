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

days = [3,1,0,0,0,0,2]
channel_id = int(os.environ.get("CHANNEL_ID"))
test_channel_id = int(os.environ.get("TEST_CHANNEL_ID"))
logfile="log.txt"

@client.event
async def on_message(message):
    if message.content == "!test":
        if message.channel.id == channel_id or message.channel.id == test_channel_id:
            await message.channel.send("Announcement Bot is Working!")
    return

async def announce(mode):
    channel = client.get_channel(channel_id)
    if mode:
        message="@everyone\n今日は定例会です！"
    else:
        message="@everyone\n明日は定例会です！"
    if channel:
        await channel.send(message)
    return

async def testannounce_morning(done):
    channel = client.get_channel(test_channel_id)
    if done:
        message="True"
    else:
        message="False"
    if channel:
        await channel.send("定時連絡(朝)\n"+message)
    return

async def testannounce_evening(done):
    channel = client.get_channel(test_channel_id)
    if done:
        message="True"
    else:
        message="False"
    if channel:
        await channel.send("定時連絡(夕方)\n"+message)
    return

async def check_time():
    done = False
    while True:
        # Morning check at 6 AM
        now = datetime.datetime.now()
        next_morning = now.replace(hour=6, minute=0, second=0, microsecond=0)
        if now >= next_morning:
            next_morning += datetime.timedelta(days=1)
        seconds_until = (next_morning - now).total_seconds()
        print(f"Sleep: {seconds_until}", file=logfile)
        await asyncio.sleep(seconds_until)
        current_time = datetime.datetime.now()
        print(f"Wake up: {current_time}", file=logfile)
        day_of_week = current_time.weekday()
        print(f"Day of week: {day_of_week}", file=logfile)
        if days[day_of_week] in [1, 3]:
            if done:
                if days[day_of_week] == 3:
                    done = False
            else:
                await announce(True)
                if days[day_of_week] == 3:
                    done = True
        await testannounce_morning(done)
        # Evening check at 6 PM
        now = datetime.datetime.now()
        next_evening = now.replace(hour=18, minute=0, second=0, microsecond=0)
        if now >= next_evening:
            next_evening += datetime.timedelta(days=1)
        seconds_until = (next_evening - now).total_seconds()
        print(f"Sleep: {seconds_until}", file=logfile)
        await asyncio.sleep(seconds_until)
        current_time = datetime.datetime.now()
        print(f"Wake up: {current_time}", file=logfile)
        day_of_week = current_time.weekday()
        print(f"Day of week: {day_of_week}", file=logfile)
        if days[day_of_week] in [2, 3]:
            if not done:
                await announce(False)
        await testannounce_evening(done)

@client.event
async def on_ready():
    print("Bot is ready!")
    await check_time()

client.run(TOKEN)
