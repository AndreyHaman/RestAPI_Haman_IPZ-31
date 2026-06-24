import time
import uuid
import os
import redis.asyncio as redis
from fastapi import Request, HTTPException

RATE_LIMITS = {
    "anonymous": (2, 60),
    "authenticated": (10, 60),
}

redis_client: redis.Redis = None 

async def init_redis():
    global redis_client
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_client = redis.from_url(redis_url, decode_responses=True)

async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()

async def rate_limit(request: Request, user_id: str | None = None):
    global redis_client
    if not redis_client:
        return

    identity = user_id if user_id else request.client.host 
    limit_type = "authenticated" if user_id else "anonymous" 
    limit, period = RATE_LIMITS[limit_type]

    key = f"rate_limit_{identity}"
    now = int(time.time())
    window_start = now - period

    async with redis_client.pipeline(transaction=True) as pipe:
        pipe.zremrangebyscore(key, min=0, max=window_start)
        pipe.zcard(key)
        member = f"{now}_{uuid.uuid4()}"
        pipe.zadd(key, {member: now})
        pipe.expire(key, period)
        results = await pipe.execute()
    
    request_count = results[1]
    
    if request_count >= limit:
        raise HTTPException(status_code=429, detail="Too many requests")