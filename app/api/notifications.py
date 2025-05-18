from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.notification import NotificationRequest, NotificationResponse
from app.store.in_memory import InMemoryStore
from app.services.dispatcher import dispatch_notification

router = APIRouter()

@router.post(
    "/notifications",
    response_model=NotificationResponse,
    summary="Send a notification to a user",
    response_description="Notification sent successfully"
)
def send_notification(payload: NotificationRequest):
    try:
        dispatch_notification(payload)
        return {"status": "success", "message": "Notification sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/users/{user_id}/notifications",
    response_model=List[dict],
    summary="Get in-app notifications for a user",
    response_description="List of in-app notifications"
)
def get_user_notifications(user_id: str):
    try:
        notifications = InMemoryStore.get_notifications(user_id)
        return notifications
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
