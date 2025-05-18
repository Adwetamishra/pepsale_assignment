# Variables
PROJECT_NAME = notification-service
IMAGE_NAME = $(PROJECT_NAME)
PORT = 8000

# Build Docker image
.PHONY: docker-build
docker-build:
	docker build -t $(IMAGE_NAME) .

# Run Docker container
.PHONY: docker-run
docker-run:
	docker run -p $(PORT):8000 $(IMAGE_NAME)

# Run tests
.PHONY: test
test:
	docker exec -it notification-service bash -c "pip install pytest httpx && PYTHONPATH=/app pytest tests/"

# Run the worker in Docker
.PHONY: docker-worker
docker-worker:
	docker exec -it notification-service bash -c "PYTHONPATH=/app python app/queue/consumer.py"
