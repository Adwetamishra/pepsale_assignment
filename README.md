# Notification Service

A notification service built with **FastAPI** and **RabbitMQ**, supporting **email**, **SMS**, and **in-app** notifications.

## Features

- `POST /api/notifications`: Send email, SMS, or in-app notifications
- `GET /api/users/{userId}/notifications`: Fetch in-app notifications for a user
- Asynchronous processing using RabbitMQ
- In-memory storage for in-app notifications
- Docker-based setup
- Unit tests included

---

## Prerequisites

- Docker & Docker Compose
- Python 3.11+

---

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd notification-service
   ```

2. **Start the app and RabbitMQ**:
   ```bash
   docker-compose up --build -d
   ```

3. **Run the background worker**:
   ```bash
   make docker-worker
   ```

## Testing

```bash
make test
```

## API Endpoints

### 1. Send a Notification
**Endpoint:** `POST /api/notifications`

**Request:**
```json
{
  "userId": "user123",
  "type": "in-app",  // "email" or "sms" also supported
  "message": "Your notification message",
  "subject": "Optional for email"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Notification sent"
}
```

### 2. Get In-App Notifications
**Endpoint:** `GET /api/users/{userId}/notifications`

**Response:**
```json
[
  {
    "type": "in-app",
    "message": "Your notification message"
  }
]
```

## Architecture

### High-Level Flow
- **POST /api/notifications** accepts a notification request.
- FastAPI pushes the request to RabbitMQ.
- A background worker listens to RabbitMQ and:
  - For in-app: stores the message in memory per user
  - For email: logs the email (Improvement we can do: can be integrated with SendGrid, etc.)
  - For sms: logs the SMS (Improvement we can do: can be integrated with Twilio, etc.)
- **GET /api/users/{userId}/notifications** fetches stored in-app messages.

### Note
- RabbitMQ handles all async processing.
- Email/SMS are printed to console (mocked) and not stored.
- We are using an in-memory database for simplicity. This can be improved by integrating a relational database or any other database solution.

## API Documentation
For detailed API documentation, visit [API Docs](http://localhost:8001/docs).
