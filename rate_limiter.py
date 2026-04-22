import logging
from redis_manager import RedisManager
from utils.async_utils import run_async  # <-- import the wrapper

logger = logging.getLogger(__name__)

class RateLimiter:

    @staticmethod
    def check_limit(key: str, max_requests: int, window_seconds: int):
        try:
            current = run_async(RedisManager.increment(key))

            # Fix: use expire instead of set_key to avoid overwriting counter
            if current == 1:
                run_async(RedisManager.expire(key, window_seconds))

            remaining = max(0, max_requests - current)
            allowed = current <= max_requests

            status = "ALLOWED" if allowed else "BLOCKED"
            logger.info(
                f"[RateLimiter] {status} | {key} | "
                f"{current}/{max_requests} | remaining={remaining}"
            )
            return allowed, remaining

        except Exception as e:
            logger.error(f"[RateLimiter ERROR] {key}: {e}")
            return True, -1

    @staticmethod
    def get_remaining(key: str, max_requests: int) -> int:
        try:
            current = run_async(RedisManager.get_key(key))
            current_count = int(current) if current else 0
            return max(0, max_requests - current_count)
        except Exception as e:
            logger.error(f"[RateLimiter get_remaining ERROR] {e}")
            return max_requests

    @staticmethod
    def reset_limit(key: str) -> bool:
        try:
            run_async(RedisManager.delete_key(key))
            logger.info(f"[RateLimiter] Reset limit for {key}")
            return True
        except Exception as e:
            logger.error(f"[RateLimiter reset ERROR] {key}: {e}")
            return False