from fastapi import FastAPI
from database import engine, Base
from routers.user_routes import user_router
from routers.project_routes import project_router
from routers.task_routes import task_router
from routers import role_routes, permission_routes
from routers.premium_router import router as premium_router
from routers import plan_router, payment_router, subscription_router, webhook_router
from routers.auth_router import auth_router

app = FastAPI()

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

@app.get("/")
def welcome():
    return {"message": "Mini Project Management System"}


@app.get("/payment-success")
def payment_success(session_id: str | None = None):
    return {
        "message": "Payment completed successfully",
    }

