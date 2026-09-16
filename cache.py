import asyncio
import time

class TTLCache:
    def __init__(self, max_size=1000, default_ttl=300):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache = {}
        self._timestamps = {}
        self._access_times = {}

    def get(self, key, ttl=None):
        if key in self._cache:
            age = time.time() - self._timestamps.get(key, 0)
            if age < (ttl or self.default_ttl):
                self._access_times[key] = time.time()
                return self._cache[key]
            else:
                self._evict(key)
        return None

    def set(self, key, value, ttl=None):
        if len(self._cache) >= self.max_size:
            self._evict_oldest()
        self._cache[key] = value
        self._timestamps[key] = time.time()
        self._access_times[key] = time.time()

    def delete(self, key):
        self._evict(key)

    def clear(self):
        self._cache.clear()
        self._timestamps.clear()
        self._access_times.clear()

    def _evict(self, key):
        self._cache.pop(key, None)
        self._timestamps.pop(key, None)
        self._access_times.pop(key, None)

    def _evict_oldest(self):
        if not self._access_times:
            return
        oldest_key = min(self._access_times, key=self._access_times.get)
        self._evict(oldest_key)

    def _evict_expired(self):
        now = time.time()
        expired = [k for k, t in self._timestamps.items() if now - t >= self.default_ttl]
        for k in expired:
            self._evict(k)

    @property
    def size(self):
        return len(self._cache)

class BotCache:
    def __init__(self):
        self.users = TTLCache(max_size=500, default_ttl=300)
        self.guilds = TTLCache(max_size=100, default_ttl=600)
        self.channels = TTLCache(max_size=200, default_ttl=120)
        self.roles = TTLCache(max_size=300, default_ttl=300)

    def get_user(self, user_id):
        return self.users.get(user_id)

    def set_user(self, user_id, data):
        self.users.set(user_id, data)

    def get_guild(self, guild_id):
        return self.guilds.get(guild_id)

    def set_guild(self, guild_id, data):
        self.guilds.set(guild_id, data)

    def get_channels(self, guild_id):
        return self.channels.get(guild_id)

    def set_channels(self, guild_id, data):
        self.channels.set(guild_id, data)

    def get_roles(self, guild_id):
        return self.roles.get(guild_id)

    def set_roles(self, guild_id, data):
        self.roles.set(guild_id, data)

    def invalidate_user(self, user_id):
        self.users.delete(user_id)

    def invalidate_guild(self, guild_id):
        self.guilds.delete(guild_id)
        self.channels.delete(guild_id)
        self.roles.delete(guild_id)

    def clear_all(self):
        self.users.clear()
        self.guilds.clear()
        self.channels.clear()
        self.roles.clear()

    def stats(self):
        return {
            "users": self.users.size,
            "guilds": self.guilds.size,
            "channels": self.channels.size,
            "roles": self.roles.size,
        }

    def cleanup_all(self):
        self.users._evict_expired()
        self.guilds._evict_expired()
        self.channels._evict_expired()
        self.roles._evict_expired()

bot_cache = BotCache()
