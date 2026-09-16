import discord
from discord.ext import commands
import psutil
import time
import platform
from datetime import datetime

class LanhDiaSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.version = "6.1.0"

    # --- Thuật thức 1: .lanhdia (Menu chính theo style JJK ông thích) ---
    @commands.command(name="lanhdia")
    async def _lanhdia_menu(self, ctx):
        p = self.bot.command_prefix
        menu = f"""```ansi
\033[1;35m💫 DOMAIN EXPANSION: INFINITE VOID 💫\033[0m
\033[1;37m**Lãnh địa đã sẵn sàng!** Chọn thuật thức bên dưới:\033[0m

\033[1;31m⚔️ WAR\033[0m     \033[1;30m  {p}raid\033[0m    \033[1;30m- Menu chiến tranh\033[0m
\033[1;34m🎵 MUSIC\033[0m   \033[1;30m  {p}nhac\033[0m   \033[1;30m- Menu nhạc\033[0m
\033[1;32m🎮 FUN\033[0m     \033[1;30m  {p}traloi\033[0m \033[1;30m- Menu giải trí\033[0m
\033[1;33m🛠️ UTILITY\033[0m  \033[1;30m  {p}chucu\033[0m  \033[1;30m- Menu tiện ích\033[0m
\033[1;35m🛡️ ADMIN\033[0m   \033[1;30m  {p}quanly\033[0m \033[1;30m- Menu quản lý\033[0m
\033[1;36m🃏 TROLL\033[0m   \033[1;30m  {p}troll\033[0m  \033[1;30m- Menu troll\033[0m

\033[1;30mJJK-VVNK Bot | {len(self.bot.guilds)} servers\033[0m
```"""
        await ctx.send(menu)
        await ctx.send("https://cdn.discordapp.com/attachments/1447965096214007872/1449264465970331789/C4A0F6F1-28DA-4945-AE12-4A258A305084.gif")

    # --- Thuật thức 2: .info (Bảng thông số kỹ thuật style diff) ---
    @commands.command(name="info")
    async def _bot_info(self, ctx):
        try:
            # Tính toán Uptime chính xác
            uptime_delta = datetime.fromtimestamp(time.time()) - datetime.fromtimestamp(self.start_time)
            days = uptime_delta.days
            hours, remainder = divmod(uptime_delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
            
            ping = round(self.bot.latency * 1000)
            
            diff_style = f"""```diff
+ {self.version}
- Bot Name: {self.bot.user.name}
- Bot ID: {self.bot.user.id}
- Total Servers: {len(self.bot.guilds)}
- Bot Latency: {ping}ms
- Uptime: {uptime_str}
- Host Python Version: {platform.python_version()}
- Discord.py Version: {discord.__version__}
```"""
            await ctx.send(diff_style)
        except Exception as e:
            print(f"Lỗi .info: {e}")

async def setup(bot):
    await bot.add_cog(LanhDiaSystem(bot))