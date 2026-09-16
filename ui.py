import discord
from discord.ext import commands
import asyncio
import time

class UIHelper:
    @staticmethod
    def progress_bar(current, total, length=20):
        filled = int(length * current / total) if total > 0 else 0
        bar = "█" * filled + "░" * (length - filled)
        percent = int(100 * current / total) if total > 0 else 0
        return f"`[{bar}] {percent}%`"

class UISystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="menu")
    async def _main_menu(self, ctx):
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

    @commands.command(name="warmenu")
    async def _war_menu(self, ctx):
        p = self.bot.command_prefix
        menu = f"""```ansi
\033[1;31m⚔️ DOMAIN EXPANSION: CHIẾN TRANH ⚔️\033[0m
\033[1;37m**Chọn thuật thức tấn công:**\033[0m

\033[1;35m⚡ SPAM (100 tin)\033[0m
\033[1;30m  {p}vohahan [delay] [text]  \033[1;30m- Spam tùy chỉnh\033[0m
\033[1;30m  {p}thuong [delay]         \033[1;30m- Spam ngon.txt\033[0m
\033[1;30m  {p}lienke [delay] [@tag]  \033[1;30m- Spam nhay.txt\033[0m
\033[1;30m  {p}hacmon [url] [d] [t]  \033[1;30m- Webhook spam\033[0m

\033[1;34m🔊 VOICE\033[0m
\033[1;30m  {p}ngucmon [id]           \033[1;30m- Treo Voice\033[0m
\033[1;30m  {p}loanvuc [id] [d]      \033[1;30m- Spam join/leave\033[0m

\033[1;31m🧨 DESTROY\033[0m
\033[1;30m  {p}khaitram              \033[1;30m- Xóa kênh\033[0m
\033[1;30m  {p}huydiet               \033[1;30m- Nuke server\033[0m
\033[1;30m  {p}anpham [so] [emoji]   \033[1;30m- Reaction spam\033[0m

\033[1;33m⚠️ Gõ {p}ngung để dừng tất cả!\033[0m
```"""
        await ctx.send(menu)

    @commands.command(name="musicmenu")
    async def _music_menu(self, ctx):
        p = self.bot.command_prefix
        menu = f"""```ansi
\033[1;34m🎵 PHÁP ĐÀN AM THANH 🎵\033[0m
\033[1;37m**Chọn bài hát:**\033[0m

\033[1;34m🎶 PHÁT NHẠC\033[0m
\033[1;30m  {p}play [link/ten]        \033[1;30m- YouTube\033[0m
\033[1;30m  {p}play-sa               \033[1;30m- Stay Alive\033[0m
\033[1;30m  {p}play-sh               \033[1;30m- Styx Helix\033[0m
\033[1;30m  {p}play-amk              \033[1;30m- Akuma no Ko\033[0m
\033[1;30m  {p}play-sp               \033[1;30m- Specialz\033[0m

\033[1;32m📋 ĐIỀU KHIỂN\033[0m
\033[1;30m  {p}queue / skip / stop   \033[1;30m- Hàng đợi\033[0m
\033[1;30m  {p}now / loop            \033[1;30m- Đang phát\033[0m
\033[1;30m  {p}pause / resume        \033[1;30m- Tạm dừng\033[0m
\033[1;30m  {p}volume [1-100]        \033[1;30m- Âm lượng\033[0m
```"""
        await ctx.send(menu)

    @commands.command(name="funmenu")
    async def _fun_menu(self, ctx):
        p = self.bot.command_prefix
        menu = f"""```ansi
\033[1;32m🎮 PHÁP ĐÀN GIẢI TRÍ 🎮\033[0m
\033[1;37m**Chọn thuật thức:**\033[0m

\033[1;34m🎮 MINI GAMES\033[0m
\033[1;30m  {p}8ball / rps / trivia  \033[1;30m- Games\033[0m
\033[1;30m  {p}coinflip / number    \033[1;30m- Đoán số\033[0m

\033[1;32m💰 KINH TẾ\033[0m
\033[1;30m  {p}daily / bal / pay    \033[1;30m- Vàng\033[0m
\033[1;30m  {p}shop / inventory     \033[1;30m- Cửa hàng\033[0m

\033[1;33m🌟 VUI\033[0m
\033[1;30m  {p}fact / quote / meme  \033[1;30m- Vui\033[0m
\033[1;30m  {p}insult / compliment  \033[1;30m- Troll\033[0m
\033[1;30m  {p}avatar / banner      \033[1;30m- Ảnh\033[0m
```"""
        await ctx.send(menu)

    @commands.command(name="progress")
    async def _test_progress(self, ctx, current: int = 50, total: int = 100):
        bar = UIHelper.progress_bar(current, total)
        await ctx.send(f"📊 **Progress:** {bar}")

async def setup(bot):
    await bot.add_cog(UISystem(bot))
