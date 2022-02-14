#coding UTF-8
import discord
from discord.ext import commands
import json
import os
import watch_later


token = str()
with open('token.json','r') as t:
    token = json.load(t)

#建立機器人
bot = commands.Bot(command_prefix = "!hey ")

#機器人啟動時觸發
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
    finale = watch_later.get_watch_later()
    await ctx.send(finale)


#啟動機器人
if __name__ == "__main__":
    bot.run(token['token'])