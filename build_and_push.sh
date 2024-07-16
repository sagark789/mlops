#!/bin/bash
repository_uri=609324725328.dkr.ecr.us-east-2.amazonaws.com/maven_mlops_test

# Authenticate Docker to your ECR repository
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin $repository_uri

# Build your Docker image
docker build -t mlops .

docker buildx create --use
docker buildx build --platform linux/amd64 -t mlops --load .


# Tag your Docker image
docker tag mlops:latest $repository_uri:latest

# Push the image to ECR
docker push $repository_uri:latest
