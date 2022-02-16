#coding UTF-8
import discord
from discord.ext import commands, tasks
import keep_alive
import json
import os
import system.watch_later as watch_later
import system.youtube as youtube


# 讀token
token = str()
with open('token.json','r') as t:
    token = json.load(t)


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
        await ctx.send("新增成功")
    else:
        await ctx.send("新增失敗")


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
    for creator in finale_list:
        for text in creator:
            await ctx.send(text)


@tasks.loop(minutes=1)
async def check_update():
    await bot.wait_until_ready()
    channel = bot.get_channel(943126423911145472)

    finale_list = youtube.check_latest()
    if finale_list:
        for creator in finale_list:
            for text in creator:
                await channel.send(text)


check_update.start()
keep_alive.keep_alive()

# 啟動機器人
if __name__ == "__main__":
    bot.run(token['token'])