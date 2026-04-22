from fastapi import FastAPI
from database import engine, Base
from routers.user_routes import user_router
from routers.project_routes import project_router
from routers.task_routes import task_router
from routers import role_routes, permission_routes
from routers.premium_router import router as premium_router
from routers import plan_router, payment_router, subscription_router, webhook_router
from routers.auth_router import auth_router
from redis_manager import RedisManager
from websocket.routes import router as websocket_router

app = FastAPI()

import logging

logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_redis():
    logger.info("App starting up...")
    try:
        await RedisManager.connect()
        logger.info(" Redis connected")
    except Exception as e:
        logger.error(f" Redis connection failed: {e}")
        raise



Base.metadata.create_all(bind=engine)


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(role_routes.role_router)
app.include_router(permission_routes.permission_router)
app.include_router(plan_router.router)
app.include_router(payment_router.router)
app.include_router(subscription_router.router)
app.include_router(webhook_router.router)
app.include_router(premium_router, prefix="/premium", tags=["Premium"])
app.include_router(websocket_router)


@app.on_event("shutdown")
async def shutdown_redis():
    logger.info(" App shutting down...")
    try:
        await RedisManager.disconnect()
        logger.info(" Redis disconnected")
    except Exception as e:
        logger.error(f" Redis shutdown error: {e}")

@app.get("/")
def welcome():
    return {"message": "Mini Project Management System"}


@app.get("/health")
async def health_check():
    redis_healthy = await RedisManager.check_health()

    return {
        "status": "healthy" if redis_healthy else "degraded",
        "redis": "connected" if redis_healthy else "disconnected",
        "app": "running"
    }