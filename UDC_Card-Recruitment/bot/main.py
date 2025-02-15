import discord
from discord.ext import commands
import os

# 初期設定
TOKEN = os.getenv("TOKEN")
intent = discord.Intents.default()
intent.message_content= True
client = commands.Bot(
    command_prefix='!',
    intents=intent
)
channel_id = int(os.environ.get("CHANNEL_ID"))
test_channel_id = int(os.environ.get("TEST_CHANNEL_ID"))

# データ構造
recruitment = {}
# {person: {want:str, num:int, active:bool}}
transaction = {}
# {transaction-number: {person-from:str, person-to:str, card:str, num:int, active:bool}}

async def check_channel(ctx):
    if ctx.channel.id == channel_id or ctx.channel.id == test_channel_id:
        return True
    else:
        return False

# コマンド
@client.command()
async def help(ctx):
    if await check_channel(ctx):
        await ctx.send(
            "```"
            "【募集】\n"
            "!want [カード名] [枚数]\n"
            "【確認】\n"
            "!check [カード名/人](個別確認)\n"
            "!check (引数なしで全体確認)\n"
            "【取引追加】(募集した人が合意後に実行する)\n"
            "!trade [取引相手] [カード名] [枚数]\n"
            "【募集終了】\n"
            "!end [カード名]\n"
            "【取引完了】\n"
            "!done [取引番号]\n"
            "【進行中の取引一覧】\n"
            "!list\n"
            "```"
        )
@client.command()
async def want(ctx, *args):
    if await check_channel(ctx):
        if len(args) == 2:
            person = ctx.author.name
            want = args[0]
            if num.isdecimal():
                num = int(args[1])
                if person in recruitment.keys():
                    if recruitment[person]["active"]:
                        recruitment[person]["num"] += num
                        recruitment[person]["active"] = True
                    else:
                        recruitment[person] = {"person":person, "want":want, "num":num, "active":True}
                return
        await ctx.send("登録方法に誤りがあります。")
@client.command()
async def check(ctx, *args):
    text=""
    if await check_channel(ctx):
        if len(args) == 0:
            for key in recruitment.keys():
                buffa={}
                if recruitment[key]["active"]:
                    if key in buffa.keys():
                        buffa[key].append([recruitment[key]["want"], recruitment[key]["num"]])
                    else:
                        buffa[key] = [[recruitment[key]["want"], recruitment[key]["num"]]]
            for key in buffa.keys():
                text += f"{key}さんの募集一覧\n"
                for i in range(len(buffa[key])):
                    text += f"・{buffa[key][i][0]} ×{buffa[key][i][1]}\n"
        elif len(args) == 1:
            buffa={}
            for key in recruitment.keys():
                if key == args[0]:
                    if recruitment[key]["active"]:
                        if key in buffa.keys():
                            buffa[key].append([recruitment[key]["want"], recruitment[key]["num"]])
                        else:
                            buffa[key] = [[recruitment[key]["want"], recruitment[key]["num"]]]
            if buffa=={}:
                for key in recruitment.keys():
                    if recruitment[key]["want"] == args[0]:
                        if recruitment[key]["active"]:
                            if recruitment[key]["want"] in buffa:
                                buffa[recruitment[key]["want"]].append([key, recruitment[key]["num"]])
                            else:
                                buffa[recruitment[key]["want"]] = [[key, recruitment[key]["num"]]]
                for key in buffa.keys():
                    text += f"「{key}」への募集一覧\n"
                    for i in range(len(buffa[key])):
                        text += f"・{buffa[key][i][0]}：{buffa[key][i][1]}枚\n"
            else:
                for key in buffa.keys():
                    text += f"{key}さんの募集一覧\n"
                    for i in range(len(buffa[key])):
                        text += f"・{buffa[key][i][0]} ×{buffa[key][i][1]}\n"
        else:
            text += "確認方法に誤りがあります。\n"
        text = text[:-1]
        await ctx.send(text)
@client.command()
async def trade(ctx, *args):
    if await check_channel(ctx):
        if len(args) == 3:
            transaction_number = str(len(transaction.keys())+1)
            person_from = args[0]
            person_to = ctx.author.name
            card = args[1]
            if args[2].isdecimal():
                num = int(args[2])
                if person_from in recruitment.keys():
                    if recruitment[person_from]["active"]:
                        if recruitment[person_from]["want"] == card and recruitment[person_from]["num"] >= num:
                            transaction[transaction_number] = {"person-from":person_from, "person-to":person_to, "card":card, "num":num, "active":True}
                            await ctx.send(f"取引{transaction_number} を登録しました。")
            return
        await ctx.send("取引登録方法に誤りがあります。")
@client.command()
async def end(ctx, *args):
    if await check_channel(ctx):
        if len(args) == 1:
            card = args[0]
            for key in recruitment.keys():
                if recruitment[key]["want"] == card:
                    recruitment[key]["active"] = False
            await ctx.send(f"{ctx.author.name}さんが{card} の募集を終了しました。")
        else:
            await ctx.send("募集終了方法に誤りがあります。")
@client.command()
async def done(ctx, *args):
    if await check_channel(ctx):
        if len(args) == 1:
            if args[0] in transaction.keys():
                if transaction[args[0]]["active"]:
                    transaction[args[0]]["active"] = False
                    await ctx.send(f"取引{args[0]}が完了しました。")
                else:
                    await ctx.send("既に完了している取引です。")
            else:
                await ctx.send("該当する取引が存在しません。")
        else:
            await ctx.send("取引完了方法に誤りがあります。")
@client.command()
async def list(ctx, *args):
    if await check_channel(ctx):
        text=""
        if await check_channel(ctx):
            for key in transaction.keys():
                if transaction[key]["active"]:
                    text += f"取引{key}：{transaction[key]['person-from']} → {transaction[key]['person-to']}：{transaction[key]['card']} ×{transaction[key]['num']}\n"
            text = text[:-1]
            await ctx.send(text)
@client.command()
async def test(ctx):
    if ctx.channel.id == channel_id or ctx.channel.id == test_channel_id:
        await ctx.send("Card-Recruitment Bot is Working!")
@client.event
async def on_ready():
    print("Bot is ready!")

client.run(TOKEN)
