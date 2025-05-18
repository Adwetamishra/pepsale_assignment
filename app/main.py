from fastapi import FastAPI
from app.api.notifications import router as notification_router

def create_app() -> FastAPI:
    app = FastAPI(title="Notification Service")

    app.include_router(notification_router, prefix="/api", tags=["Notifications"])

    @app.get("/")
    def read_root():
        return {"message": "Notification Service is running"}

    return app
