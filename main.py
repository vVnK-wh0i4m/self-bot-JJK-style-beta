import os
import sys
import json
import re
import asyncio
import aiohttp

# Fix CWD: ensure project dir is in sys.path for cog loading
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_DIR)
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

import discord
from discord.ext import commands
from pytz import timezone

import rate_utils

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

settings = load_settings()

# --- 1. CAU HINH: uu tien Bien moi truong, fallback config.json ---
TOKEN = os.environ.get("DISCORD_TOKEN") or os.environ.get("DISCORD_BOT_TOKEN") or os.environ.get("BOT_TOKEN")
PREFIX = "."

if not TOKEN and os.path.exists('config.json'):
    with open('config.json', 'r', encoding='utf-8-sig') as f:
        config = json.load(f)
    TOKEN = config.get('token') or config.get('Token')

if not TOKEN:
    if not os.path.exists('config.json'):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump({"token": "DAN_TOKEN_VAO_DAY", "prefix": PREFIX}, f, indent=4)
    print("\033[1;31m[!] Khong tim thay Token!\033[0m")
    print("\033[1;33m  -> Cach 1: dat Bien moi truong DISCORD_TOKEN\033[0m")
    print("\033[1;33m  -> Cach 2: dan Token vao config.json roi chay lai\033[0m")
    sys.exit(1)

# --- 2. BIEN TRANG THAI ---
vietnam_tz = timezone('Asia/Ho_Chi_Minh')
active_features = {
    'cyclestatus': True,
    'auto_react': False,
    'thuong': False,
    'he': False,
    'forcedisconnect': False,
    'nitro_sniper': True
}

# --- 3. GIF RESPONSES ---
gif_responses = settings.get("gif_responses", {})
auto_gif = settings.get("auto_gif", True)

def get_gif(category):
    if not auto_gif:
        return None
    return gif_responses.get(category)

# --- 4. HEADER VIP ---
def get_main_headers():
    return {
        'accept': '*/*',
        'authorization': TOKEN,
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.1072 Chrome/120.0.6099.291 Safari/537.36',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJwdGIiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC4xMDcyIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDQiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjEwNzIgQ2hyb21lLzEyMC4wLjYwOTkuMjkxIEVsZWN0cm9uLzI4LjIuMTAgU2FmYXJpLzUzNy4zNiJ9'
    }

# --- 5. KHỞI TẠO BOT ---
bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)

# --- 6. GIF COMMAND CATEGORIES ---
COMMAND_GIF_MAP = {
    'vohahan': 'spam', 'thuong': 'spam', 'lienke': 'spam', 'hacmon': 'spam',
    'khaitram': 'nuke', 'huydiet': 'nuke', 'diet': 'nuke',
    'ngucmon': 'raid', 'loanvuc': 'raid', 'anpham': 'raid',
    'nhac': 'music', 'play': 'music', 'play-sa': 'music', 'play-sh': 'music',
    'play-amk': 'music', 'play-sp': 'music',
    '8ball': 'fun', 'rps': 'fun', 'trivia': 'fun', 'coinflip': 'fun',
    'number': 'fun', 'fact': 'fun', 'quote': 'fun', 'meme': 'fun',
    'batdiet': 'troll', 'xucxac': 'troll', 'amhon': 'troll', 'truhon': 'troll',
    'fake': 'troll', 'donguyen': 'troll', 'vonghon': 'troll',
    'nguyenrua': 'troll', 'batkhuat': 'troll',
    'tram': 'admin', 'phong': 'admin', 'giai': 'admin',
    'tao': 'admin', 'danh': 'admin',
}

# --- 7. AUTO DELETE USER MESSAGES ---
@bot.event
async def on_message(message):
    try:
        if active_features.get('nitro_sniper'):
            if message.author == bot.user:
                pass
            elif 'discord.gift/' in message.content or 'discordapp.com/gifts/' in message.content:
                match = re.search(r"(discord\.gift\/|discordapp\.com\/gifts\/)(\w+)", message.content)
                if match:
                    code = match.group(2)
                    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}/redeem"
                    resp = None
                    async with aiohttp.ClientSession() as session:
                        for _ in range(3):
                            async with session.post(url, headers=get_main_headers()) as resp:
                                if resp.status != 429:
                                    break
                                await rate_utils.handle_429_response(resp)
                    if resp is not None and resp.status == 200:
                        print(f"\033[1;32m[+] DA HUP DUOC NITRO: {code}\033[0m")
                    else:
                        print(f"\033[1;31m[-] Hut Nitro: {code}\033[0m")
    except Exception as e:
        print(f"\033[1;31m[Nitro Error] {e}\033[0m")

    await bot.process_commands(message)

    # Xoa tin nhan prefix SAU khi xu ly xong
    if message.author != bot.user and message.content.startswith(PREFIX):
        try:
            await message.delete()
        except Exception:
            pass

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    bot_name = settings.get("bot_name", "HostBot")
    author = settings.get("author", "QU4N.TH3.D3V")
    banner = f"""\033[1;33m
                  {author}\033[0m
\033[1;36m    ██╗   ██╗██╗   ██╗███╗   ██╗██╗  ██╗   \033[0m
\033[1;36m    ██║   ██║██║   ██║████╗  ██║██║ ██╔╝   \033[0m
\033[1;36m    ██║   ██║██║   ██║██╔██╗ ██║█████╔╝    \033[0m
\033[1;36m    ╚██╗ ██╔╝╚██╗ ██╔╝██║╚██╗██║██╔═██╗    \033[0m
\033[1;36m     ╚████╔╝  ╚████╔╝ ██║ ╚████║██║  ██╗   \033[0m
\033[1;36m      ╚═══╝    ╚═══╝  ╚═╝  ╚═══╝╚═╝  ╚═╝   \033[0m
    """
    print(banner)
    print(f"\033[1;36m[>] Bot:\033[0m \033[1;32m{bot.user}\033[0m")
    print(f"\033[1;36m[>] ID:\033[0m \033[1;32m{bot.user.id}\033[0m")
    print(f"\033[1;36m[>] Servers:\033[0m \033[1;32m{len(bot.guilds)}\033[0m")
    print(f"\033[1;36m[>] Prefix:\033[0m \033[1;32m{PREFIX}\033[0m")
    print(f"\033[1;36m{'-'*54}\033[0m")

    skip = {'main.py', 'index.py', 'rate_utils.py', 'cache.py', '__init__.py', 'console.py'}
    for filename in os.listdir('.'):
        if filename.endswith('.py') and filename not in skip:
            try:
                await bot.load_extension(filename[:-3])
                print(f"\033[1;32m    + Da nap thuat thuc: {filename}\033[0m")
            except Exception as e:
                print(f"\033[1;31m    - Loi nap {filename}: {e}\033[0m")

    print(f"\033[1;35m{'-'*54}\033[0m")
    print(f"\033[1;32m[SUCCESS] {bot_name} da san sang. Go {PREFIX}menu de mo Menu.\033[0m")

    if active_features.get('cyclestatus'):
        asyncio.create_task(cycle_status())

# --- 8. STATUS CYCLING ---
async def cycle_status():
    await bot.wait_until_ready()
    cycle = settings.get("status_cycle", [])
    if not cycle:
        return
    idx = 0
    while not bot.is_closed():
        try:
            text = cycle[idx % len(cycle)]
            await bot.change_presence(activity=discord.Game(name=text))
            idx += 1
            await asyncio.sleep(10)
        except Exception:
            await asyncio.sleep(5)

# --- 9. AUTO GIF AFTER COMMANDS ---
@bot.event
async def on_command_completion(ctx):
    if not auto_gif:
        return
    cmd_name = ctx.command.name if ctx.command else None
    if not cmd_name:
        return
    category = COMMAND_GIF_MAP.get(cmd_name)
    if category:
        gif_url = get_gif(category)
        if gif_url:
            try:
                await ctx.send(gif_url)
            except Exception:
                pass

# --- 10. KHOI CHAY ---
async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\033[1;31m\n[!] HostBot da dung.\033[0m")
    except Exception as e:
        print(f"\033[1;31m[!] Loi he thong: {e}\033[0m")
