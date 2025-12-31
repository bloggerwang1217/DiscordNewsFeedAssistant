#coding UTF-8
"""
Discord News Feed Bot (Lite)
Only Email and RSS features
"""
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import system.email_grabber as email
import system.rss_reader as rss

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!hey ", intents=intents)


def split_message(text, limit=1900):
    """Split long message into chunks under Discord's limit"""
    if len(text) <= limit:
        return [text]
    chunks = []
    while text:
        chunks.append(text[:limit])
        text = text[limit:]
    return chunks


async def safe_send(target, text):
    """Send message, splitting if too long"""
    for chunk in split_message(str(text)):
        await target.send(chunk)


@bot.event
async def on_ready():
    print(f">> Bot is ready << Logged in as {bot.user}")
    if not check_update.is_running():
        check_update.start()


# ===== Email Commands =====

@bot.command()
async def 看最新信件(ctx):
    """Get latest email"""
    finale_list = email.get_latest_email()
    for item in finale_list:
        if type(item) == list:
            for text in item:
                await safe_send(ctx, text)
        else:
            await safe_send(ctx, item)


# ===== RSS Commands =====

@bot.command()
async def 追蹤rss(ctx, name, link):
    """Add RSS feed"""
    finale = rss.add_rss(name, link)
    if finale:
        await ctx.send("追蹤成功")
    else:
        await ctx.send("追蹤失敗")


@bot.command()
async def 取消rss(ctx, name):
    """Remove RSS feed"""
    finale = rss.remove_rss(name)
    if finale:
        await ctx.send("取消成功")
    else:
        await ctx.send("取消失敗")


@bot.command()
async def 用rss看(ctx, name, index):
    """Read RSS feed entry"""
    finale_list = rss.get_rss(name, int(index))
    for line in finale_list:
        await safe_send(ctx, line)


# ===== Auto Check (every 1 minute) =====

@tasks.loop(minutes=15)
async def check_update():
    await bot.wait_until_ready()
    channel_id = os.environ.get("DISCORD_CHANNEL_ID")
    if not channel_id:
        print("Warning: DISCORD_CHANNEL_ID not set")
        return
    channel = bot.get_channel(int(channel_id))

    # Check new email
    finale_list = email.check_latest()
    if finale_list:
        for item in finale_list:
            if type(item) == list:
                for text in item:
                    await safe_send(channel, text)
            else:
                await safe_send(channel, item)

    # Check new RSS
    finale_list = rss.check_latest()
    if finale_list:
        for website in finale_list:
            for line in website:
                await safe_send(channel, line)


if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        print("Error: DISCORD_TOKEN not set in .env")
    else:
        bot.run(token)
