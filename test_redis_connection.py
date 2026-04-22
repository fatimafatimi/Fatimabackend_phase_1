import redis
import redis.asyncio as aioredis
import asyncio

# ============ TEST 1: Synchronous Connection ============
print("=" * 50)
print("TEST 1: Synchronous Redis Connection")
print("=" * 50)

try:
    # Sync Redis
    r = redis.Redis(
        host='localhost',
        port=6379,
        db=0,
        decode_responses=True
    )
    
    response = r.ping()
    print(f"✅ Connected to Redis: {response}")
    
    r.set('test_key', 'Hello from Python!')
    print("✅ Set value: test_key = 'Hello from Python!'")
    
    value = r.get('test_key')
    print(f"✅ Retrieved value: {value}")
    
    r.delete('test_key')
    print("✅ Deleted key: test_key")
    
except Exception as e:
    print(f"❌ Error: {e}")

print()

# ============ TEST 2: Async Connection ============
print("=" * 50)
print("TEST 2: Async Redis Connection (FastAPI)")
print("=" * 50)

async def test_async_redis():
    try:
        redis_client = aioredis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )
        
        response = await redis_client.ping()
        print(f"✅ Async Connected to Redis: {response}")
        
        await redis_client.set('async_test', 'Hello Async!')
        print("✅ Set value (async)")
        
        value = await redis_client.get('async_test')
        print(f"✅ Retrieved value (async): {value}")
        
        await redis_client.delete('async_test')
        print("✅ Deleted key (async)")
        
        await redis_client.close()
        print("✅ Connection closed")
        
    except Exception as e:
        print(f"❌ Error: {e}")

asyncio.run(test_async_redis())

print()
print("=" * 50)
print("All tests completed!")
print("=" * 50)