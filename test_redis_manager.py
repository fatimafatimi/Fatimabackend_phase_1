import asyncio
from redis_manager import RedisManager

async def test():
    print("Testing RedisManager...")
    
    # Connect
    print("1. Connecting to Redis...")
    await RedisManager.connect()
    
    # Set a key
    print("2. Setting a key...")
    await RedisManager.set_key("test:message", "Hello Redis!")
    
    # Get the key
    print("3. Getting the key...")
    value = await RedisManager.get_key("test:message")
    print(f"   Value: {value}")
    
    # Check if exists
    print("4. Checking if key exists...")
    exists = await RedisManager.key_exists("test:message")
    print(f"   Exists: {exists}")
    
    # Delete the key
    print("5. Deleting the key...")
    await RedisManager.delete_key("test:message")
    
    # Disconnect
    print("6. Disconnecting...")
    await RedisManager.disconnect()
    
    print("✅ All tests passed!")

# Run test
asyncio.run(test())
