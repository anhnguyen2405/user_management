#!/bin/bash

# Build Docker images
docker build -t auth_service ./auth_service
docker build -t user_service ./user_service
docker build -t ui_service ./ui_service

# Start microservices using Docker Compose
docker-compose up
