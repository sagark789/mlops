# Bash Script for Building and Pushing Docker Images to ECR

This section provides an explanation of the Bash script, which is used to build a Docker image and push it to Amazon ECR (Elastic Container Registry).

## Overview

The script performs the following key tasks:
1. Authenticates Docker to your ECR repository.
2. Builds the Docker image.
3. Tags the Docker image.
4. Pushes the Docker image to ECR.

### Script Breakdown

- **#!/bin/bash**: Specifies the script interpreter.
- **repository_uri**: Sets the URI of the ECR repository.
```bash
#!/bin/bash
repository_uri=609324725328.dkr.ecr.us-east-2.amazonaws.com/maven_mlops_test
```

- Authenticates Docker to your ECR repository using the AWS CLI.
```bash
# Authenticate Docker to your ECR repository
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin $repository_uri
```

- Builds the Docker image using `docker build`.
- Creates a new builder instance and sets it as the current builder using `docker buildx create --use`.
- Builds the Docker image for the specified platform using `docker buildx build`.
```bash
# Build your Docker image
docker build -t mlops .

docker buildx create --use
docker buildx build --platform linux/amd64 -t mlops --load .
```

- Tags the Docker image with the repository URI.
```bash
# Tag your Docker image
docker tag mlops:latest $repository_uri:latest
```

- Pushes the tagged Docker image to the ECR repository.
```bash
# Push the image to ECR
docker push $repository_uri:latest
```

By following this script, you can automate the process of building and pushing Docker images to Amazon ECR.
