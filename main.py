#coding UTF-8
from discord.ext import commands, tasks
import keep_alive
import json
import os
from datetime import datetime
import system.watch_later as watch_later
import system.youtube as youtube
import system.twitch as twitch
import system.email_grabber as email
import system.eth_tracker as coin
import system.rss_reader as rss


# Read token from environment variable
token = os.environ.get("DISCORD_TOKEN")


# 建立機器人
bot = commands.Bot(command_prefix = "!hey ")

# 機器人啟動時觸發
@bot.event
async def on_ready():

    # game = discord.Activity(type = discord.ActivityType.playing,name = '$hrpg help for help.' )
    # await bot.change_presence(status=discord.Status.online, activity=game)
    
    print(">> bot is ready <<")

# #導入指令功能

# for filename in os.listdir('cmds'):
#     if filename[-3::]  == '.py':
#         bot.load_extension(F"cmds.{filename[:-3]}")

@bot.command()
async def 之後要看(ctx, name, link):
    finale = watch_later.add_watch_later(name, link)
    if finale:
        await ctx.send("新增成功")
    else:
        await ctx.send("新增失敗")


@bot.command()
async def 移除(ctx, name):
    finale = watch_later.remove_watch_later(name)
    if finale:
        await ctx.send("移除成功")
    else:
        await ctx.send("移除失敗")


@bot.command()
async def 要看啥(ctx):
    finale_list = watch_later.get_watch_later()
    for item in finale_list:
        for text in item:
            await ctx.send(text)


@bot.command()
async def 追蹤頻道(ctx, link):
    finale = youtube.add_channel(link)
    if finale:
        await ctx.send("追蹤成功")
    else:
        await ctx.send("追蹤失敗")


@bot.command()
async def 移除頻道(ctx, link):
    finale = youtube.remove_channel(link)
    if finale:
        await ctx.send("移除成功")
    else:
        await ctx.send("移除失敗")


@bot.command()
async def 看最新貼文(ctx):
    finale_list = youtube.get_latest_post()
    for creator in finale_list:
        for text in creator:
            await ctx.send(text)


@bot.command()
async def 看最新影片(ctx):
    finale_list = youtube.get_latest_video()
    for text in finale_list:
        await ctx.send(text)


@bot.command()
async def 追蹤直播(ctx, link):
    finale = twitch.add_channel(link)
    if finale:
        await ctx.send("追蹤成功")
    else:
        await ctx.send("追蹤失敗")


@bot.command()
async def 退追直播(ctx, link):
    finale = twitch.remove_channel(link)
    if finale:
        await ctx.send("退追成功")
    else:
        await ctx.send("退追失敗")


@bot.command()
async def 看最新信件(ctx):
    finale_list = email.get_latest_email()
    for item in finale_list:
        if type(item) == list:
            for text in item:
                await ctx.send(text)
        else:
            await ctx.send(item)


@bot.command()
async def 看以太幣(ctx):
    await ctx.send(coin.get_eth_price())


@bot.command()
async def 追蹤rss(ctx, name, link):
    finale = rss.add_rss(name, link)
    if finale:
        await ctx.send("追蹤成功")
    else:
        await ctx.send("追蹤失敗")


@bot.command()
async def 取消rss(ctx, name):
    finale = rss.remove_rss(name)
    if finale:
        await ctx.send("取消成功")
    else:
        await ctx.send("取消失敗")


@bot.command()
async def 用rss看(ctx, name, index):
    finale_list = rss.get_rss(name, int(index))

    for line in finale_list:
        await ctx.send(line)


@tasks.loop(minutes=1)
async def check_update():
    await bot.wait_until_ready()
    channel = bot.get_channel(943126423911145472)
    update_time = ["07:00", "10:00", "14:00", "16:00"]  # 換成格林威治時間
  
    current_time = datetime.now().strftime("%H:%M")  

    if current_time in update_time:
        await channel.send(coin.get_eth_price())

    finale_list = youtube.check_latest()
    if finale_list:
        for creator in finale_list:
            if type(creator) == str:
                await channel.send(creator)
            else:
                for text in creator:
                    await channel.send(text)
  
    finale_list = twitch.check_latest()
    if finale_list:
        for text in finale_list:
            await channel.send(text)

    finale_list = email.check_latest()
    if finale_list:
        for item in finale_list:
            if type(item) == list:
                for text in item:
                    await channel.send(text)
            else:
                await channel.send(item)

    finale_list = rss.check_latest()
    if finale_list:
        for website in finale_list:
            for line in website:
                await channel.send(line)


check_update.start()
# keep_alive.keep_alive()

# 啟動機器人
if __name__ == "__main__":
    bot.run(token)