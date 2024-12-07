import discord
from discord.ext import commands
import asyncio
import os
import requests
from bs4 import BeautifulSoup

TOKEN =  os.getenv("TOKEN")
# 入賞数ランキング
DISCORD_CHANNEL_ID= int(os.environ.get("DISCORD_CHANNEL_ID"))
# 新カード
DISCORD_CHANNEL_ID_2= int(os.environ.get("DISCORD_CHANNEL_ID_2"))
# CS結果
DISCORD_CHANNEL_ID_3= int(os.environ.get("DISCORD_CHANNEL_ID_3"))
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")
intent = discord.Intents.default()
intent.message_content= True

client = commands.Bot(
    command_prefix='-',
    intents=intent
)

# youtubeのapiは一日あたり10000回まで。1分1回で1440回なので余裕
search_url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={YOUTUBE_CHANNEL_ID}&part=id&order=date"
denen_url="https://supersolenoid.jp/blog-category-12.html"

# 起動前に更新しておく
latest_video="9r13OIuDcTY"
latest_articles=['https://supersolenoid.jp/blog-entry-40291.html', 'https://supersolenoid.jp/blog-entry-40520.html', 'https://supersolenoid.jp/blog-entry-40550.html', 'https://supersolenoid.jp/blog-entry-40518.html', 'https://supersolenoid.jp/blog-entry-40547.html', 'https://supersolenoid.jp/blog-entry-40546.html', 'https://supersolenoid.jp/blog-entry-40544.html', 'https://supersolenoid.jp/blog-entry-40545.html', 'https://supersolenoid.jp/blog-entry-40548.html', 'https://supersolenoid.jp/blog-entry-40543.html', 'https://supersolenoid.jp/blog-entry-40549.html', 'https://supersolenoid.jp/blog-entry-40542.html', 'https://supersolenoid.jp/blog-entry-40541.html', 'https://supersolenoid.jp/blog-entry-40466.html', 'https://supersolenoid.jp/blog-entry-40540.html']

async def get_new_video():
    response = requests.get(search_url)
    data = response.json()
    video_id = data["items"][0]["id"]["videoId"]
    return video_id

async def check_new_video():
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    global latest_video
    new_video = await get_new_video()
    if new_video != latest_video:
        latest_video = [new_video]
        await channel.send(f"https://www.youtube.com/watch?v={new_video}")

async def get_new_articles():
    response = requests.get(denen_url)
    soup = BeautifulSoup(response.text, "html.parser")
    article = soup.find_all("div",class_="EntryTitle")
    articles = []
    for a in article:
        articles.append(a.find("a").get("href"))
    article_title = soup.find_all("div",class_="EntryTitle")
    article_titles = []
    for t in article_title:
        article_titles.append(t.find("a").text)
    return articles, article_titles

async def ranking_check(new_article):
    response = requests.get(new_article)
    soup = BeautifulSoup(response.text, "html.parser")
    ranking_img = soup.find("div",class_="EntryTitle").find("img").get("src")
    return ranking_img

async def result_check(new_article):
    response = requests.get(new_article)
    soup = BeautifulSoup(response.text, "html.parser")
    # <a name="more" id="more"></a>の次のdivタグの中に画像がある
    result_div = soup.find("a", id="more").find_next("div")
    # <br> タグを \n に置き換え
    for br in result_div.find_all("br"):
        br.replace_with("\n")
    # テキストを取得
    result_sentence = result_div.text
    result_names = soup.find_all("p", class_="dm_deck_name")
    names = [name.text for name in result_names]
    # 複数の画像を含む <img> 要素を取得
    result_imgs = soup.find_all("div", class_="dm_deck_image")
    imgs = [img.find("img").get("src") for img in result_imgs if img.find("img") is not None]
    return result_sentence, names, imgs

async def newcard_check(new_article):
    response = requests.get(new_article)
    soup = BeautifulSoup(response.text, "html.parser")
    newcard= soup.find_all("div",class_="card_image")
    newcard_img = [img.find("img").get("src") for img in newcard if img.find("img") is not None]
    return newcard_img

async def check_new_article():
    global latest_articles
    new_articles, article_titles = await get_new_articles()
    page_length=len(new_articles)
    for i in range(page_length):
        new_article=new_articles[i]
        article_title=article_titles[i]
        if new_article not in latest_articles:
            latest_articles = [new_article]+latest_articles[:page_length-1]
            if "入賞数ランキング" in article_title:
                channel = client.get_channel(DISCORD_CHANNEL_ID)
                await channel.send(new_article)
                await channel.send(await ranking_check(new_article))
            elif "が優勝" in article_title:
                channel = client.get_channel(DISCORD_CHANNEL_ID_3)
                result_sentence, names, imgs = await result_check(new_article)
                txt=result_sentence+"\n"
                for name in names:
                    txt+=("\n"+name)
                await channel.send(txt)
                for img in imgs:
                    await channel.send(img)
            elif "が公開" in article_title:
                channel = client.get_channel(DISCORD_CHANNEL_ID_2)
                newcard_img = await newcard_check(new_article)
                for img in newcard_img:
                    await channel.send(img)
    return

@client.command()
async def test(ctx):
    if ctx.channel.id == DISCORD_CHANNEL_ID:
        await ctx.send("Information bot is working!")

@client.event
async def on_ready():
    print("Bot is ready!")
    while True:
        await check_new_article()
        await asyncio.sleep(60)

client.run(TOKEN)