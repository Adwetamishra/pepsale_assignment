from fastapi.testclient import TestClient
from app.main import create_app
import time

client = TestClient(create_app())

def test_send_in_app_notification():
    response = client.post("/api/notifications", json={
        "userId": "test_user_1",
        "type": "in-app",
        "message": "This is a test message"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_get_in_app_notifications():
    user_id = "test_user_2"
    test_message = "This is a test message"
    response = client.post("/api/notifications", json={
        "userId": user_id,
        "type": "in-app",
        "message": test_message
    })
    assert response.status_code == 200
    max_retries = 10
    for i in range(max_retries):
        response = client.get(f"/api/users/{user_id}/notifications")
        if response.status_code == 200:
            notifications = response.json()
            if notifications and notifications[0]["message"] == test_message:
                break
        time.sleep(0.5)
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0, "No notifications found after retries"
    assert response.json()[0]["message"] == test_message
