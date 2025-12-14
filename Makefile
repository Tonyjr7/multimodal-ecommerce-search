# Makefile for AI E-commerce Search

.PHONY: help install run docker-build docker-run docker-stop clean test lint format

# Default target
help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make run          - Run the application locally"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make docker-stop  - Stop Docker container"
	@echo "  make compose-up   - Start with docker-compose"
	@echo "  make compose-down - Stop docker-compose"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean temporary files"

# Install dependencies
install:
	pip install --upgrade pip
	pip install -r requirements.txt

# Run locally
run:
	python main.py

# Docker commands
docker-build:
	docker build -t ai-ecommerce:latest .

docker-run:
	docker run -d \
		--name ai-ecommerce \
		-p 5000:5000 \
		--env-file .env \
		-v $$(pwd)/ecommerce_cnn_model.h5:/app/ecommerce_cnn_model.h5:ro \
		-v $$(pwd)/class_names.pkl:/app/class_names.pkl:ro \
		-v $$(pwd)/datasets:/app/datasets:ro \
		ai-ecommerce:latest

docker-stop:
	docker stop ai-ecommerce
	docker rm ai-ecommerce

docker-logs:
	docker logs -f ai-ecommerce

# Docker Compose commands
compose-up:
	docker-compose up -d

compose-down:
	docker-compose down

compose-logs:
	docker-compose logs -f

compose-rebuild:
	docker-compose up --build -d

# Development commands
test:
	@echo "Running tests..."
	# Add test commands here when tests are implemented
	# pytest tests/

lint:
	@echo "Running linters..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	@echo "Formatting code..."
	black .

# Clean temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Health check
health:
	curl http://localhost:5000/health

# View logs
logs:
	tail -f *.log

# Setup environment
setup:
	cp .env.example .env
	@echo "Please edit .env file with your configuration"
