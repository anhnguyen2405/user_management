#!/bin/bash

# Set Kubernetes context to your EKS cluster
# kubectl config use-context Cluster3

# Build Docker images
docker build -t ntnanh/auth_service ./auth_service
docker build -t ntnanh/user_service ./user_service
docker build -t ntnanh/ui_service ./ui_service

# # Push Docker images to a container registry (if needed)
# docker push ntnanhw1/auth_service
# docker push ntnanhw1/user_service
# docker push ntnanhw1/ui_service

# Apply Kubernetes deployments and services
kubectl apply -f kubernetes/auth_service_deploy.yaml
kubectl apply -f kubernetes/user_service_deploy.yaml
kubectl apply -f kubernetes/ui_service_deploy.yaml

kubectl apply -f kubernetes/auth_service_service.yaml
kubectl apply -f kubernetes/user_service_service.yaml
kubectl apply -f kubernetes/ui_service_service.yaml
