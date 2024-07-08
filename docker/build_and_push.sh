#!/bin/bash

# Set your public ECR repository URI
repository_uri=public.ecr.aws/f3l2h4y6/mlops

aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/f3l2h4y6

# Build the Docker image from the project root
docker build -t mlops .

# Tag the Docker image
docker tag mlops:latest public.ecr.aws/f3l2h4y6/mlops:latest

# Push the Docker image to ECR
docker push public.ecr.aws/f3l2h4y6/mlops:latest

echo "Docker image has been pushed to ECR: $repository_uri:latest"