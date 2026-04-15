import time
from collections import defaultdict, deque

from redis import Redis
from redis.exceptions import RedisError


class SmartRateLimiter:
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        limit: int = 5,
        window_seconds: int = 60,
    ) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self.source = "memory"
        self._memory_store: dict[str, deque[float]] = defaultdict(deque)

        try:
            self.redis = Redis.from_url(redis_url, decode_responses=True)
            self.redis.ping()
            self.source = "redis"
        except RedisError:
            self.redis = None

    def _memory_prune(self, key: str, now: float) -> deque[float]:
        entries = self._memory_store[key]
        while entries and entries[0] <= now - self.window_seconds:
            entries.popleft()
        return entries

    def check(self, key: str) -> dict:
        now = time.time()

        if self.redis is not None:
            return self._check_redis(key, now)

        entries = self._memory_prune(key, now)
        allowed = len(entries) < self.limit
        if allowed:
            entries.append(now)

        remaining = max(self.limit - len(entries), 0)
        reset_in = (
            int(self.window_seconds - (now - entries[0])) if entries else self.window_seconds
        )

        return {
            "allowed": allowed,
            "limit": self.limit,
            "remaining": remaining,
            "reset_in_seconds": max(reset_in, 0),
            "source": self.source,
        }

    def _check_redis(self, key: str, now: float) -> dict:
        bucket = f"rate-limit:{key}"
        window_start = now - self.window_seconds

        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(bucket, 0, window_start)
        pipe.zcard(bucket)
        _, current_count = pipe.execute()

        allowed = current_count < self.limit
        if allowed:
            member = f"{now}"
            pipe = self.redis.pipeline()
            pipe.zadd(bucket, {member: now})
            pipe.expire(bucket, self.window_seconds)
            pipe.execute()
            current_count += 1

        oldest = self.redis.zrange(bucket, 0, 0, withscores=True)
        reset_in = self.window_seconds
        if oldest:
            reset_in = int(self.window_seconds - (now - oldest[0][1]))

        return {
            "allowed": allowed,
            "limit": self.limit,
            "remaining": max(self.limit - current_count, 0),
            "reset_in_seconds": max(reset_in, 0),
            "source": self.source,
        }
