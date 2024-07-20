# GitHub Actions Workflow for Building and Pushing Docker Images to ECR

This section provides an explanation of the GitHub Actions workflow file, which is used to build a Docker image and push it to Amazon ECR (Elastic Container Registry).

## Overview

The workflow file defines the steps to:
1. Check out the code.
2. Set up QEMU for cross-platform builds.
3. Set up Docker Buildx for advanced build capabilities.
4. Install the AWS CLI.
5. Log in to Amazon ECR.
6. Build and push the Docker image to Amazon ECR.

### Workflow File Breakdown

- **name**: Specifies the name of the workflow.
- **on**: Defines the event that triggers the workflow. In this case, `workflow_dispatch` allows the workflow to be manually triggered.
```yaml
name: Build and Push to ECR

on:
  workflow_dispatch:
```

- **jobs**: Defines a job named `build_and_push_to_ecr`.
- **runs-on**: Specifies the type of runner to use (`ubuntu-latest`).
- **steps**: Lists the steps to be executed in the job.
- **Checkout code**: Uses the `actions/checkout@v2` action to check out the repository code.
```yaml
jobs:
  build_and_push_to_ecr:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2
```

- **Set up QEMU**: Uses the `docker/setup-qemu-action@v2` action to enable cross-platform builds.
```yaml
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v2
```

- **Set up Docker Buildx**: Uses the `docker/setup-buildx-action@v2` action to set up Docker Buildx.
```yaml
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
```

- **Install AWS CLI**: Installs the AWS CLI on the runner.
```yaml
      - name: Install AWS CLI
        run: |
          sudo apt-get update
          sudo apt-get install -y awscli
```

- **Log in to Amazon ECR**: Logs in to Amazon ECR using the AWS CLI. The AWS credentials and region are retrieved from the GitHub Secrets.
```yaml
      - name: Log in to Amazon ECR
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: us-east-2
        run: |
          aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin 609324725328.dkr.ecr.us-east-2.amazonaws.com
```

- **Build and push Docker image to Amazon ECR**: Builds and pushes the Docker image to Amazon ECR. The `ECR_REGISTRY`, `ECR_REPOSITORY`, and `IMAGE_TAG` environment variables are used to define the image name and tag.
  - `docker build`: Builds the Docker image.
  - `docker buildx build --platform linux/amd64 --load`: Uses Docker Buildx to build the image for the specified platform.
  - `docker push`: Pushes the Docker image to the specified ECR repository.
```yaml
      - name: Build and push Docker image to Amazon ECR
        env:
          ECR_REGISTRY: 609324725328.dkr.ecr.us-east-2.amazonaws.com
          ECR_REPOSITORY: maven_mlops_test
          IMAGE_TAG: latest
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker buildx build --platform linux/amd64 -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG --load .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
```
By following this workflow, you can automate the process of building and pushing Docker images to Amazon ECR using GitHub Actions.
