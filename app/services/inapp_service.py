from app.store.in_memory import InMemoryStore

def send_in_app(payload):
    InMemoryStore.add_notification(payload.userId, {
        "message": payload.message,
        "type": "in-app"
    })
