# DiscordNewsFeedAssistant

A Discord bot that helps you get access to contents you don't want to check manually.

## Versions

| File | Status | Description |
|------|--------|-------------|
| `main_lite.py` | **Active** | Email + RSS only, tested and working |
| `main.py` | Deprecated | Full features, last maintained in 2022 |

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

```env
DISCORD_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_channel_id
EMAIL_USERNAME=your_email_username
EMAIL_PASSWORD=your_email_password
EMAIL_SERVER=msa.ntu.edu.tw
```

### 3. Run the bot

```bash
python main_lite.py
```

## Commands (main_lite.py)

### Email

- `!hey 看最新信件` - Get latest email

### RSS Reader

- `!hey 追蹤rss <name> <url>` - Subscribe to RSS feed
- `!hey 取消rss <name>` - Unsubscribe
- `!hey 用rss看 <name> <number>` - Read article (1 = latest)

Auto-check runs every 15 minutes.

## Deploy to Server (e.g. Linode)

### 1. Clone and setup

```bash
git clone https://github.com/yourusername/DiscordNewsFeedAssistant.git
cd DiscordNewsFeedAssistant

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env  # Fill in your credentials
```

### 2. Run with systemd (recommended)

Create service file:

```bash
sudo nano /etc/systemd/system/discord-bot.service
```

```ini
[Unit]
Description=Discord News Feed Bot
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/DiscordNewsFeedAssistant
ExecStart=/path/to/DiscordNewsFeedAssistant/venv/bin/python main_lite.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable discord-bot
sudo systemctl start discord-bot
sudo systemctl status discord-bot  # Check status
```

---

## Legacy Commands (main.py)

> **Note:** These may not work with current discord.py version.

### Watch Later

- `!hey 之後要看 <name> <url>` - Add to watch later
- `!hey 移除 <name>` - Remove
- `!hey 要看啥` - List all

### YouTube

- `!hey 追蹤頻道 <url>` - Follow channel
- `!hey 移除頻道 <url>` - Unfollow
- `!hey 看最新貼文` - Get latest post
- `!hey 看最新影片` - Get latest video

### Twitch

- `!hey 追蹤直播 <url>` - Follow streamer
- `!hey 退追直播 <url>` - Unfollow

### ETH Price

- `!hey 看以太幣` - Get ETH price
