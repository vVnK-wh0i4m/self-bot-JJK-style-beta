import discord
from discord.ext import commands
import asyncio
import aiohttp
import platform

from rate_utils import (
    PROTECTED_GUILD_IDS,
    delete_channel_via_api,
    discord_action_with_retry,
    wait_off_429,
)

class ChucuSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sao_semaphore = asyncio.BoundedSemaphore(4)

    # ================= MENU CHÚ CỤ (JJK STYLE) =================

    @commands.command(name="chucu")
    async def _chucu_menu(self, ctx):
        p = self.bot.command_prefix
        menu = f"""```ansi
\033[1;33m🛠️ PHÁP BẢO HỖ TRỢ 🛠️\033[0m
\033[1;37m**Chọn pháp bảo:**\033[0m

\033[1;33m⚡ THUILTIN\033[0m
\033[1;30m  {p}thauthi [token]       \033[1;30m- Check token\033[0m
\033[1;30m  {p}thanhduyet [so]       \033[1;30m- Xóa tin nhắn\033[0m
\033[1;30m  {p}giapan               \033[1;30m- Đóng DM\033[0m

\033[1;34m🔊 THÔNG TIN\033[0m
\033[1;30m  {p}nguonluc             \033[1;30m- Check ping\033[0m
\033[1;30m  {p}truytung [@tag]      \033[1;30m- Soi avatar\033[0m
\033[1;30m  {p}phian [@tag]         \033[1;30m- Soi banner\033[0m

\033[1;35m🧿 ĐẶC BIỆT\033[0m
\033[1;30m  {p}sao-an [server_id]   \033[1;30m- Sao chép kênh\033[0m
\033[1;30m  {p}danhdinh [@tag]      \033[1;30m- Info user\033[0m
\033[1;30m  {p}ketgioi              \033[1;30m- Info server\033[0m
\033[1;30m  {p}dongan [emoji]       \033[1;30m- Sao chép emoji\033[0m
```"""
        await ctx.send(menu)

# ================= LÕI THỰC THI (VIẾT MỚI) =================

    @commands.command(name="thauthi")
    async def _thauthi(self, ctx, token: str):
        """[Thấu Thị] Kiểm tra linh lực Token"""
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.get('https://discord.com/api/v9/users/@me', headers=headers) as r:
                if r.status == 200:
                    data = await r.json()
                    u_tag = f"{data['username']}#{data.get('discriminator', '0')}"
                    u_id = data.get('id')
                    nitro = "Có" if data.get('premium_type') else "Không"
                    res = f"""```ansi
\033[1;32m✅ LINH LỰC XÁC NHẬN (LIVE)\033[0m
\033[1;37m- Danh tính:\033[0m {u_tag}
\033[1;37m- ID Chú linh:\033[0m {u_id}
\033[1;37m- Chú cụ (Nitro):\033[0m {nitro}
```"""
                    await ctx.send(res, delete_after=15)
                else:
                    await ctx.send("```ansi\n\033[1;31m❌ CHÚ CỤ VÔ DỤNG (TOKEN DIE)\033[0m```", delete_after=5)

    @commands.command(name="thanhduyet")
    async def _thanhduyet(self, ctx, limit: int):
        """[Thanh Duyệt] Xóa tin nhắn bản thân"""
        count = 0
        async for msg in ctx.channel.history(limit=limit):
            if msg.author.id == self.bot.user.id:
                try:
                    await msg.delete()
                    count += 1
                except discord.HTTPException as e:
                    if getattr(e, "status", None) == 429:
                        await wait_off_429(e)
                except Exception:
                    continue
        await ctx.send(f"✅ **Thanh Duyệt** hoàn tất! Đã thanh trừng `{count}` tin nhắn.", delete_after=3)

    @commands.command(name="giapan")
    async def _giapan(self, ctx):
        """[Giải Ấn] Đóng tất cả DMs"""
        count = 0
        for channel in self.bot.private_channels:
            try:
                await channel.close()
                count += 1
            except discord.HTTPException as e:
                if getattr(e, "status", None) == 429:
                    await wait_off_429(e)
            except Exception:
                continue
        await ctx.send(f"✅ **Giải Ấn** thành công! Đã đóng `{count}` cuộc hội thoại.", delete_after=5)

    @commands.command(name="nguonluc")
    async def _nguonluc(self, ctx):
        """[Nguồn Lực] Check Ping & Hệ thống"""
        ms = round(self.bot.latency * 1000)
        sys_info = platform.system()
        await ctx.send(f"```ansi\n\033[1;36m🌀 NGUỒN LỰC\033[0m\n- Chú lực trễ: {ms}ms\n- Cốt lõi hệ thống: {sys_info}```", delete_after=10)

    @commands.command(name="truytung")
    async def _truytung(self, ctx, target: discord.Member = None):
        """[Truy Tung] Soi Avatar"""
        target = target or ctx.author
        url = target.avatar.url if target.avatar else "Đối tượng không có ảnh đại diện!"
        await ctx.send(url)

    @commands.command(name="phian")
    async def _phian(self, ctx, target: discord.User = None):
        """[Phi Ấn] Soi Banner"""
        target = target or ctx.author
        try:
            user = await self.bot.fetch_user(target.id)
            if user.banner:
                await ctx.send(user.banner.url)
            else:
                await ctx.send("❌ Đối tượng không có ảnh bìa (Banner)!", delete_after=3)
        except Exception:
            await ctx.send("❌ Không thể phi ấn đối tượng này!", delete_after=3)

    @commands.command(name="sao-an")
    async def _saoan(self, ctx, server_id: int):
        """[Sao Ấn] Tái tạo toàn bộ cấu trúc kênh từ server khác"""
        source_guild = self.bot.get_guild(server_id)
        if not source_guild:
            return await ctx.send("❌ Không thể tìm thấy kết giới (Server ID) này!", delete_after=3)

        if ctx.guild.id in PROTECTED_GUILD_IDS:
            return await ctx.send("🛡️ **Kết giới đang được bảo vệ!**", delete_after=3)

        # Thanh trừng kênh cũ trong server hiện tại qua API (tránh rate limit)
        token = self.bot.http.token
        async with aiohttp.ClientSession() as session:
            tasks = [
                delete_channel_via_api(session, ch.id, token, self.sao_semaphore)
                for ch in ctx.guild.channels
            ]
            await asyncio.gather(*tasks)

        # Tái tạo danh mục và kênh
        await ctx.send(f"🌀 **Sao Ấn Khai Triển!** Đang sao chép từ: `{source_guild.name}`", delete_after=5)

        for category in source_guild.categories:
            new_cat = await discord_action_with_retry(ctx.guild.create_category, name=category.name)
            for text_ch in category.text_channels:
                await discord_action_with_retry(ctx.guild.create_text_channel, name=text_ch.name, category=new_cat)
            for voice_ch in category.voice_channels:
                await discord_action_with_retry(ctx.guild.create_voice_channel, name=voice_ch.name, category=new_cat)

    @commands.command(name="danhdinh")
    async def _danhdinh(self, ctx, target: discord.Member = None):
        """[Danh Tính] Thông tin người dùng"""
        target = target or ctx.author
        created = target.created_at.strftime('%d/%m/%Y')
        res = f"""```ansi
\033[1;34m👤 DANH TÍNH CHÚ LINH\033[0m
- Tên: {target.name}
- ID: {target.id}
- Ngày khởi tạo: {created}
```"""
        await ctx.send(res)

    @commands.command(name="ketgioi")
    async def _ketgioi(self, ctx):
        """[Kết Giới] Thông số Server"""
        g = ctx.guild
        res = f"""```ansi
\033[1;31m🏰 THÔNG SỐ KẾT GIỚI\033[0m
- Tên: {g.name}
- ID: {g.id}
- Quân số: {g.member_count} thành viên
```"""
        await ctx.send(res)

    @commands.command(name="dongan")
    async def _dongan(self, ctx, emoji: discord.PartialEmoji):
        """[Đóng Ấn] Sao chép Emoji về server"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(emoji.url) as r:
                    img = await r.read()
                    new = await discord_action_with_retry(ctx.guild.create_custom_emoji, name=emoji.name, image=img)
                    await ctx.send(f"✅ Đã đóng ấn thành công Emoji: {new}", delete_after=5)
        except Exception:
            await ctx.send("❌ Không thể đóng ấn Emoji này vào lãnh địa!", delete_after=3)

# Dòng này phải để ngoài class và ở cuối file
async def setup(bot):
    await bot.add_cog(ChucuSystem(bot))