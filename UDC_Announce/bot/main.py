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
tf=False

@client.event
async def on_message(message):
    if message.content == "!test":
        if message.channel.id == channel_id or message.channel.id == test_channel_id:
            await message.channel.send(f"Announcement Bot is Working!\nstatus: {tf}")
    return

async def announce(done):
    channel = client.get_channel(channel_id)
    if done:
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
    global tf
    done=False
    while True:
        # Morning check at 6 AM
        now = datetime.datetime.now()
        next_morning = now.replace(hour=6, minute=0, second=0, microsecond=0)
        if now >= next_morning:
            next_morning += datetime.timedelta(days=1)
        seconds_until = (next_morning - now).total_seconds()
        await asyncio.sleep(seconds_until)
        current_time = datetime.datetime.now()
        day_of_week = current_time.weekday()
        if days[day_of_week] in [1, 3]:
            if done:
                if days[day_of_week] == 3:
                    done = False
            else:
                await announce(done)
                if days[day_of_week] == 3:
                    done = True
        await testannounce_morning(done)
        # Evening check at 6 PM
        now = datetime.datetime.now()
        next_evening = now.replace(hour=18, minute=0, second=0, microsecond=0)
        if now >= next_evening:
            next_evening += datetime.timedelta(days=1)
        seconds_until = (next_evening - now).total_seconds()
        await asyncio.sleep(seconds_until)
        current_time = datetime.datetime.now()
        day_of_week = current_time.weekday()
        if days[day_of_week] in [2, 3]:
            if not done:
                await announce(done)
        await testannounce_evening(done)
        tf=done

@client.event
async def on_ready():
    print("Bot is ready!")
    await check_time()

client.run(TOKEN)
