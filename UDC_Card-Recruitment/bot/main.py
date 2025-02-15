import discord
from discord.ext import commands
import os

# 初期設定
TOKEN = os.getenv("TOKEN")
intent = discord.Intents.default()
intent.message_content= True
client = commands.Bot(
    command_prefix='-',
    intents=intent
)
channel_id = int(os.environ.get("CHANNEL_ID"))
test_channel_id = int(os.environ.get("TEST_CHANNEL_ID"))

# データ構造
recruitment = {}
# {person: [{want:str, num:int, active:bool}]}
transaction = {}
# {transaction-number: {person-from:str, person-to:str, card:str, num:int, active:bool}}

async def check_channel(ctx):
    if ctx.channel.id == channel_id or ctx.channel.id == test_channel_id:
        return True
    else:
        return False

# コマンド
@client.command()
async def guide(ctx):
    if await check_channel(ctx):
        await ctx.send(
            "```"
            "【使い方を表示】\n"
            "-guide\n"
            "【募集追加】\n"
            "-want [カード名] [枚数]\n"
            "【募集確認】\n"
            "-check [カード名/人](個別確認)\n"
            "-check (引数なしで全体確認)\n"
            "【募集終了】\n"
            "-end [カード名]\n"
            "※募集の更新は「一度募集を終了して再度募集を行う」形でお願いします。\n"
            "【取引追加】(募集した人が合意後に実行する)\n"
            "-trade [取引相手] [カード名] [枚数]\n"
            "【取引完了】\n"
            "-done [取引番号]\n"
            "【進行中の取引一覧】\n"
            "-list\n"
            "```"
        )
@client.command()
async def want(ctx, *args):
    if await check_channel(ctx):
        foo = len(args)
        if foo in [2, 3]:
            if foo == 2:
                person = ctx.author.display_name
                want = args[0]
                num = args[1]
            else:
                person = args[0]
                want = args[1]
                num = args[2]
            if num.isdecimal():
                num = int(num)
                if person in recruitment:
                    flag=True
                    for i in range(len(recruitment[person])):
                        if recruitment[person][i]["want"] == want:
                            recruitment[person][i]["num"] += num
                            recruitment[person][i]["active"] = True
                            flag=False
                    if flag:
                        recruitment[person].append({"want":want, "num":num, "active":True})
                else:
                    recruitment[person] = [{"want":want, "num":num, "active":True}]
                await ctx.send(f"{person}さんの募集を受け付けました：\n{want} ×{num}")
                return
        await ctx.send("募集追加方法に誤りがあります。")
@client.command()
async def check(ctx, *args):
    text=""
    if await check_channel(ctx):
        active_recruitment_number = 0
        for key in recruitment:
            for i in range(len(recruitment[key])):
                if recruitment[key][i]["active"]:
                    active_recruitment_number += 1
        if active_recruitment_number == 0:
            text = "現在進行中の募集はありません。\n"
        else:
            if len(args) == 0:
                buffa={}
                for key in recruitment:
                    for i in range(len(recruitment[key])):
                        if recruitment[key][i]["active"]:
                            if key in buffa:
                                buffa[key].append([recruitment[key][i]["want"], recruitment[key][i]["num"]])
                            else:
                                buffa[key] = [[recruitment[key][i]["want"], recruitment[key][i]["num"]]]
                for key in buffa:
                    text += f"{key}さんの募集一覧\n"
                    for i in range(len(buffa[key])):
                        text += f"・{buffa[key][i][0]} ×{buffa[key][i][1]}\n"
            elif len(args) == 1:
                buffa={}
                for key in recruitment:
                    if key == args[0]:
                        for i in range(len(recruitment[key])):
                            if recruitment[key][i]["active"]:
                                if key in buffa:
                                    buffa[key].append([recruitment[key][i]["want"], recruitment[key][i]["num"]])
                                else:
                                    buffa[key] = [[recruitment[key][i]["want"], recruitment[key][i]["num"]]]
                if buffa=={}:
                    for key in recruitment:
                        for i in range(len(recruitment[key])):
                            if recruitment[key][i]["want"] == args[0]:
                                if recruitment[key][i]["active"]:
                                    foo = recruitment[key][i]["want"]
                                    if foo in buffa:
                                        buffa[foo].append([key, recruitment[key][i]["num"]])
                                    else:
                                        buffa[foo] = [[key, recruitment[key][i]["num"]]]
                    for key in buffa:
                        text += f"「{key}」への募集一覧\n"
                        for i in range(len(buffa[key])):
                            text += f"・{buffa[key][i][0]}：{buffa[key][i][1]}枚\n"
                else:
                    for key in buffa:
                        text += f"{key}さんの募集一覧\n"
                        for i in range(len(buffa[key])):
                            text += f"・{buffa[key][i][0]} ×{buffa[key][i][1]}\n"
                if buffa=={}:
                    text = "該当する募集がありません。\n"
            else:
                text += "募集確認方法に誤りがあります。\n"
        text = text[:-1]
        await ctx.send(text)
@client.command()
async def end(ctx, *args):
    if await check_channel(ctx):
        foo = len(args)
        if foo in [1,2]:
            if foo == 1:
                bar = ctx.author.display_name
                card = args[0]
            else:
                bar = args[0]
                card = args[1]
            if bar in recruitment:
                argument = recruitment[bar]
                flag = True
                for wanted in argument:
                    if wanted["want"] == card:
                        wanted["active"] = False
                        wanted["num"] = 0
                        flag = False
                    await ctx.send(f"{bar}さんが「{card}」 の募集を終了しました。")
                if flag:
                    await ctx.send(f"{bar}さんは「{card}」 を募集していません。")
            else:
                await ctx.send(f"{bar}さんが募集しているカードはありません。")
        else:
            await ctx.send("募集終了方法に誤りがあります。")
@client.command()
async def trade(ctx, *args):
    if await check_channel(ctx):
        if len(args) == 3:
            transaction_number = str(len(transaction)+1)
            person_from = args[0]
            person_to = ctx.author.display_name
            card = args[1]
            if args[2].isdecimal():
                num = int(args[2])
                if person_to in recruitment:
                    flag=False
                    for i in range(len(recruitment[person_to])):
                        foo = recruitment[person_to][i]
                        if foo["want"] == card:
                            if foo["active"]:
                                flag=True
                                if recruitment[person_to][i]["num"] >= num:
                                    break
                                else:
                                    foo = recruitment[person_to][i]["num"]
                                    await ctx.send(f"{person_to}さんが募集している枚数({foo})を超えています。")
                                    return
                            else:
                                await ctx.send(f"{person_to}さんは「{card}」 の募集をすでに締め切っています。")
                                return
                    if flag:
                        transaction[transaction_number] = {"person-from":person_from, "person-to":person_to, "card":card, "num":num, "active":True}
                        await ctx.send(f"「取引{transaction_number}」が追加されました：\n{person_from} → {person_to} - {card} ×{num}")
                    else:
                        await ctx.send(f"{person_to}さんは「{card}」 を募集していません。")
                else:
                    await ctx.send(f"{person_to}さんが募集しているカードはありません。")
            return
        await ctx.send("取引追加方法に誤りがあります。")
@client.command()
async def done(ctx, *args):
    if await check_channel(ctx):
        if len(args) == 1:
            if args[0] in transaction:
                foo = transaction[args[0]]
                if foo["active"]:
                    foo["active"] = False
                    bar = recruitment[foo["person-from"]]
                    for i in range(len(bar)):
                        if bar[i]["want"] == foo["card"]:
                            baz = bar[i]["num"]
                            baz -= foo["num"]
                            if baz <= 0:
                                baz = 0
                                recruitment[foo["person-from"]][i]["active"] = False
                            recruitment[foo["person-from"]][i]["num"] = baz
                    await ctx.send(f"取引{args[0]}が完了しました：\n{foo['person-from']} → {foo['person-to']} - {foo['card']} ×{foo['num']}")
                else:
                    await ctx.send("既に完了している取引です。")
            else:
                await ctx.send("該当する取引が存在しません。")
        else:
            await ctx.send("取引完了方法に誤りがあります。")
@client.command()
async def list(ctx):
    if await check_channel(ctx):
        text=""
        active_transaction_number = 0
        for key in transaction:
            if transaction[key]["active"]:
                active_transaction_number += 1
        if active_transaction_number == 0:
            text = "進行中の取引はありません。"
        else:
            for key in transaction:
                if transaction[key]["active"]:
                    text += f"取引{key}：{transaction[key]['person-from']} → {transaction[key]['person-to']} - {transaction[key]['card']} ×{transaction[key]['num']}\n"
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
