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


def init_save_files():
    """Initialize save directory and required JSON files if they don't exist"""
    import json

    os.makedirs("save", exist_ok=True)

    files = {
        "latest_mail.json": {"last_count": 0},
        "followed_rss.json": {}
    }

    for filename, default in files.items():
        path = f"save/{filename}"
        if not os.path.exists(path):
            with open(path, 'w') as f:
                json.dump(default, f)


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
    init_save_files()
    print(f">> Bot is ready << Logged in as {bot.user}")
    if not check_update.is_running():
        check_update.start()


# ===== Help Command =====

@bot.command()
async def 說明(ctx):
    """Show all available commands"""
    help_text = """
📚 **Discord News Feed Bot - 指令說明**

**Email 相關**
  • `!hey 看最新信件` - 查看最新的電子郵件

**RSS Reader 相關**
  • `!hey 追蹤rss <名稱> <連結>` - 訂閱 RSS 源
  • `!hey 取消rss <名稱>` - 取消訂閱
  • `!hey 用rss看 <名稱> <編號>` - 查看文章 (1=最新)

**自動檢查**
  每 1 分鐘自動檢查新的郵件和 RSS 文章並推送到頻道

**範例**
  `!hey 追蹤rss BloggerMandolin https://bloggermandolin.com/blog/rss.xml`
  `!hey 用rss看 BloggerMandolin 1`
    """
    await safe_send(ctx, help_text)


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

@tasks.loop(minutes=1)
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
