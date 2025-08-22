# Makefile for Django Todo App Development

.PHONY: help build up down test lint clean deploy

# Default target
help:
	@echo "Available commands:"
	@echo "  help       - Show this help message"
	@echo "  build      - Build Docker containers"
	@echo "  up         - Start development environment"
	@echo "  down       - Stop development environment"
	@echo "  test       - Run tests"
	@echo "  lint       - Run code linting"
	@echo "  clean      - Clean up containers and volumes"
	@echo "  deploy     - Deploy to AWS (future)"

# Development commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

test:
	cd todoapp && python manage.py test --settings=config.django.test

lint:
	cd todoapp && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

clean:
	docker-compose down -v
	docker system prune -f

# Development setup
setup:
	pip install -r requirements.txt
	pip install flake8
	cd todoapp && python manage.py migrate --settings=config.django.test

# AWS deployment (placeholder for future)
deploy:
	@echo "AWS deployment script will be added here"
	@echo "Use: make deploy-aws for AWS deployment"
