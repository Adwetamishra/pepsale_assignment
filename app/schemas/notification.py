from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

class NotificationRequest(BaseModel):
    userId: str
    type: Literal["email", "sms", "in-app"]
    message: str
    subject: Optional[str] = None

class NotificationResponse(BaseModel):
    status: str
    message: str
