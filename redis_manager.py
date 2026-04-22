import redis.asyncio as redis
import json
import logging
from typing import Optional, Any

# Setup logging
logger = logging.getLogger(__name__)

class RedisManager:
    """
    Manages all Redis connections and operations for Mini PMS.
    
    This is a singleton - only one instance throughout the app.
    Use: await RedisManager.set_key(...) from anywhere
    """
    
    # Global Redis connection (shared across entire app)
    _redis_connection: Optional[redis.Redis] = None
    
    # ========== CONNECTION MANAGEMENT ==========
    
    @classmethod
    async def connect(cls):
        """
        Establish connection to Redis.
        Call this when FastAPI app starts.
        """
        if cls._redis_connection is None:
            try:
                cls._redis_connection = redis.Redis(
                    host="localhost",
                    port=6379,
                    decode_responses=True
                )
                
                # Test connection
                await cls._redis_connection.ping()
                logger.info("✅ Connected to Redis successfully")
                
            except Exception as e:
                logger.error(f"❌ Failed to connect to Redis: {e}")
                raise
    
    @classmethod
    async def disconnect(cls):
        """
        Close connection to Redis.
        Call this when FastAPI app shuts down.
        """
        if cls._redis_connection is not None:
            try:
                await cls._redis_connection.close()
                cls._redis_connection = None
                logger.info("✅ Disconnected from Redis")
            except Exception as e:
                logger.error(f"❌ Error disconnecting from Redis: {e}")
    
    @classmethod
    async def get_connection(cls) -> redis.Redis:
        """
        Get the Redis connection.
        If not connected, connect first.
        """
        if cls._redis_connection is None:
            await cls.connect()
        return cls._redis_connection
    
    @classmethod
    async def check_health(cls) -> bool:
        """
        Check if Redis connection is healthy.
        Returns True if connected, False otherwise.
        """
        try:
            redis = await cls.get_connection()
            await redis.ping()
            return True
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return False
    
    # ========== STRING OPERATIONS (Most Used) ==========
    
    @classmethod
    async def set_key(
        cls,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        serialize: bool = False
    ) -> bool:
        """
        Set a key-value pair in Redis.
        
        Args:
            key: The key name (e.g., "otp:user:123")
            value: The value to store
            ttl: Time to live in seconds (auto-delete after this time)
            serialize: If True, converts object to JSON
        
        Returns:
            True if successful
        
        Example:
            # Simple string
            await RedisManager.set_key("status", "active")
            
            # With expiration (5 minutes)
            await RedisManager.set_key("otp:123", "456789", ttl=300)
            
            # Object (convert to JSON)
            user_data = {"id": 1, "name": "John"}
            await RedisManager.set_key("user:1", user_data, serialize=True)
        """
        try:
            redis = await cls.get_connection()
            
            # Convert object to JSON if needed
            if serialize:
                value = json.dumps(value)
            
            # Set with TTL (time to live)
            if ttl:
                await redis.setex(key, ttl, value)
            else:
                await redis.set(key, value)
            
            logger.debug(f"Set key: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting key {key}: {e}")
            return False
    
    @classmethod
    async def get_key(
        cls,
        key: str,
        deserialize: bool = False
    ) -> Optional[Any]:
        """
        Get a value from Redis.
        
        Args:
            key: The key name
            deserialize: If True, converts JSON back to object
        
        Returns:
            The value, or None if key doesn't exist
        
        Example:
            # Get simple string
            otp = await RedisManager.get_key("otp:123")
            
            # Get object (convert from JSON)
            user = await RedisManager.get_key("user:1", deserialize=True)
        """
        try:
            redis = await cls.get_connection()
            value = await redis.get(key)
            
            if value and deserialize:
                value = json.loads(value)
            
            logger.debug(f"Got key: {key}")
            return value
            
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}")
            return None
    
    @classmethod
    async def delete_key(cls, key: str) -> int:
        """
        Delete a key from Redis.
        
        Args:
            key: The key to delete
        
        Returns:
            Number of keys deleted (1 if deleted, 0 if not found)
        
        Example:
            deleted = await RedisManager.delete_key("otp:123")
            print(f"Deleted {deleted} keys")
        """
        try:
            redis = await cls.get_connection()
            result = await redis.delete(key)
            logger.debug(f"Deleted key: {key}")
            return result
            
        except Exception as e:
            logger.error(f"Error deleting key {key}: {e}")
            return 0
    
    @classmethod
    async def key_exists(cls, key: str) -> bool:
        """
        Check if a key exists in Redis.
        
        Returns:
            True if exists, False otherwise
        
        Example:
            if await RedisManager.key_exists("otp:123"):
                print("OTP exists")
        """
        try:
            redis = await cls.get_connection()
            result = await redis.exists(key)
            return bool(result)
            
        except Exception as e:
            logger.error(f"Error checking key existence {key}: {e}")
            return False
    
    @classmethod
    async def get_ttl(cls, key: str) -> int:
        """
        Get remaining time to live (TTL) for a key.
        
        Returns:
            Seconds remaining, -1 if no TTL, -2 if key doesn't exist
        
        Example:
            ttl = await RedisManager.get_ttl("otp:123")
            print(f"OTP expires in {ttl} seconds")
        """
        try:
            redis = await cls.get_connection()
            result = await redis.ttl(key)
            return result
            
        except Exception as e:
            logger.error(f"Error getting TTL for key {key}: {e}")
            return -2
    
    # ========== COUNTER OPERATIONS (For Rate Limiting) ==========
    
    @classmethod
    async def increment(cls, key: str, amount: int = 1) -> int:
        """
        Increment a number in Redis (atomic operation).
        
        Args:
            key: The key name
            amount: How much to increment (default 1)
        
        Returns:
            New value after increment
        
        Example:
            # Increment login attempts
            attempts = await RedisManager.increment("login:attempts:user:123")
            
            # Increment by 5
            count = await RedisManager.increment("page:views:123", amount=5)
        """
        try:
            redis = await cls.get_connection()
            result = await redis.incrby(key, amount)
            logger.debug(f"Incremented {key} by {amount}, new value: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error incrementing key {key}: {e}")
            return 0
    
    @classmethod
    async def decrement(cls, key: str, amount: int = 1) -> int:
        """
        Decrement a number in Redis (atomic operation).
        
        Args:
            key: The key name
            amount: How much to decrement (default 1)
        
        Returns:
            New value after decrement
        
        Example:
            remaining = await RedisManager.decrement("attempts:user:123")
        """
        try:
            redis = await cls.get_connection()
            result = await redis.decrby(key, amount)
            logger.debug(f"Decremented {key} by {amount}, new value: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error decrementing key {key}: {e}")
            return 0
    
    # ========== LIST OPERATIONS (For Activity Feed) ==========
    
    @classmethod
    async def add_to_list(cls, key: str, *values) -> int:
        """
        Add items to the right end of a list.
        
        Args:
            key: The list key name
            values: Items to add
        
        Returns:
            Length of list after adding
        
        Example:
            # Add activity to feed
            await RedisManager.add_to_list(
                "activity:user:123",
                "Created project",
                "Invited team member"
            )
        """
        try:
            redis = await cls.get_connection()
            result = await redis.rpush(key, *values)
            logger.debug(f"Added {len(values)} items to list {key}")
            return result
            
        except Exception as e:
            logger.error(f"Error adding to list {key}: {e}")
            return 0
    
    @classmethod
    async def get_list(
        cls,
        key: str,
        start: int = 0,
        end: int = -1
    ) -> list:
        """
        Get items from a list.
        
        Args:
            key: The list key name
            start: Starting index (0 = first)
            end: Ending index (-1 = last)
        
        Returns:
            List of items
        
        Example:
            # Get last 10 activities
            activities = await RedisManager.get_list("activity:user:123", -10, -1)
            
            # Get all
            all_activities = await RedisManager.get_list("activity:user:123")
        """
        try:
            redis = await cls.get_connection()
            result = await redis.lrange(key, start, end)
            logger.debug(f"Retrieved {len(result)} items from list {key}")
            return result
            
        except Exception as e:
            logger.error(f"Error getting list {key}: {e}")
            return []
    
    # ========== SET OPERATIONS (For Token Blacklist) ==========
    
    @classmethod
    async def add_to_set(cls, key: str, *members) -> int:
        """
        Add members to a set (no duplicates).
        
        Args:
            key: The set key name
            members: Members to add
        
        Returns:
            Number of members added
        
        Example:
            # Add tokens to blacklist
            await RedisManager.add_to_set("blacklist:tokens", "token1", "token2")
        """
        try:
            redis = await cls.get_connection()
            result = await redis.sadd(key, *members)
            logger.debug(f"Added {result} members to set {key}")
            return result
            
        except Exception as e:
            logger.error(f"Error adding to set {key}: {e}")
            return 0
    
    @classmethod
    async def is_member(cls, key: str, member: str) -> bool:
        """
        Check if member exists in a set.
        
        Args:
            key: The set key name
            member: Member to check
        
        Returns:
            True if member exists, False otherwise
        
        Example:
            if await RedisManager.is_member("blacklist:tokens", user_token):
                print("Token is blacklisted!")
        """
        try:
            redis = await cls.get_connection()
            result = await redis.sismember(key, member)
            return bool(result)
            
        except Exception as e:
            logger.error(f"Error checking set membership {key}: {e}")
            return False
    
    # ========== UTILITY FUNCTIONS ==========
    
    @classmethod
    async def flush_all(cls):
        """
        ⚠️ DELETE ALL DATA IN REDIS!
        Only use for testing/development.
        """
        try:
            redis = await cls.get_connection()
            await redis.flushdb()
            logger.warning("⚠️ Flushed all Redis data")
            
        except Exception as e:
            logger.error(f"Error flushing Redis: {e}")
    
    @classmethod
    async def get_all_keys(cls, pattern: str = "*") -> list:
        """
        Get all keys matching a pattern.
        
        Args:
            pattern: Key pattern (e.g., "otp:*", "user:*")
        
        Returns:
            List of matching keys
        
        Example:
            # Get all OTP keys
            otp_keys = await RedisManager.get_all_keys("otp:*")
        """
        try:
            redis = await cls.get_connection()
            result = await redis.keys(pattern)
            logger.debug(f"Found {len(result)} keys matching {pattern}")
            return result
            
        except Exception as e:
            logger.error(f"Error getting keys with pattern {pattern}: {e}")
            return []
        
        
    @classmethod
    async def expire(cls, key: str, seconds: int) -> bool:
        try:
            redis = await cls.get_connection()
            result = await redis.expire(key, seconds)
            logger.debug(f"Set expire on {key}: {seconds}s")
            return bool(result)
        except Exception as e:
            logger.error(f"[Redis expire ERROR] {key}: {e}")
            return False