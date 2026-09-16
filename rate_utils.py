import asyncio
import json

import aiohttp
import discord

# Whitelist: thêm ID server vào đây để các lệnh phá hoại tự chặn
PROTECTED_GUILD_IDS = []

# Ngưỡng delay tối thiểu (giây) — bypass rate limit, chạy max speed
MIN_SPAM_DELAY = 0
MIN_WEBHOOK_DELAY = 0
MIN_VOICE_DELAY = 0
MIN_CREATE_DELAY = 0


async def get_retry_after(response) -> float:
    """Lấy số giây Discord yêu cầu chờ qua header hoặc body của response 429."""
    ra = response.headers.get("Retry-After")
    if ra:
        return float(ra)
    try:
        data = await response.json()
        return float(data.get("retry_after", 1.0))
    except Exception:
        return 1.0


def is_global_rate_limit(response) -> bool:
    """Kiểm tra response 429 có thuộc global bucket hay không."""
    return response.headers.get("X-RateLimit-Global", "").lower() == "true"


async def handle_429_response(response, margin=0) -> bool:
    """Ngủ đúng thời gian Discord yêu cầu khi gặp 429. Trả về True nếu gặp 429."""
    if response.status != 429:
        return False
    wait = await get_retry_after(response) + margin
    if is_global_rate_limit(response):
        wait += 0.5
    await asyncio.sleep(wait)
    return True


def retry_after_from_exception(e: discord.HTTPException) -> float:
    """Lấy retry_after từ discord.HTTPException (dùng cho lệnh gọi qua discord.py)."""
    try:
        header = e.response.headers.get("Retry-After")
        if header:
            return float(header)
        data = json.loads(getattr(e, "text", "") or "{}")
        return float(data.get("retry_after", 1.0))
    except Exception:
        return 1.5


async def wait_off_429(e: discord.HTTPException) -> None:
    """Ngủ retry_after khi bị 429 qua discord.py — tối thiểu delay."""
    await asyncio.sleep(retry_after_from_exception(e))


async def delete_channel_via_api(session, channel_id, token, semaphore, max_retries=5):
    """Xóa kênh qua API trực tiếp, tự điều tiết khi bị rate limit."""
    url = f"https://discord.com/api/v9/channels/{channel_id}"
    headers = {"Authorization": token, "Content-Type": "application/json"}
    retries = 0
    while retries < max_retries:
        async with semaphore:
            async with session.delete(url, headers=headers) as r:
                if await handle_429_response(r):
                    retries += 1
                    continue
                return r.status
    return None


async def discord_action_with_retry(func, *args, **kwargs):
    """Gọi một thao tác discord.py, tự retry khi bị 429."""
    while True:
        try:
            return await func(*args, **kwargs)
        except discord.HTTPException as e:
            if getattr(e, "status", None) == 429:
                await wait_off_429(e)
                continue
            raise