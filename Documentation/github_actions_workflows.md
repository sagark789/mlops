### GitHub Actions Workflow for Testing, Linting, and Pushing Docker Images to ECR

This guide provides a detailed explanation of two GitHub Actions workflows: one for testing and linting the code and another for building and pushing Docker images to Amazon Elastic Container Registry (ECR). These workflows help automate code quality checks and deployment processes.

---

### **Test and Lint Workflow**

#### Overview
The "Test and Lint" workflow ensures that all code changes meet quality standards by running tests and linting checks. This workflow is triggered on every push to the `main` branch and on every pull request.

#### Workflow File Breakdown

**name**: Specifies the workflow's name.
```yaml
name: Test and Lint
```

**on**: Defines the events that trigger the workflow. Here, it runs on pushes to the `main` branch and on pull requests.
```yaml
on:
  push:
    branches:
      - main
  pull_request:
```

**jobs**: Defines the `test-and-lint` job that runs on an Ubuntu runner.
```yaml
jobs:
  test-and-lint:
    runs-on: ubuntu-latest
```

**steps**: Lists the actions to perform in this job.

- **Checkout code**: Uses `actions/checkout@v2` to pull the latest code from the repository.
  ```yaml
  steps:
    - name: Checkout code
      uses: actions/checkout@v2
  ```

- **Set up Python**: Uses `actions/setup-python@v2` to set up Python 3.8 environment.
  ```yaml
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
  ```

- **Install dependencies**: Creates a virtual environment, upgrades pip, and installs the required packages, including `black`, `flake8`, and `pytest`.
  ```yaml
    - name: Install dependencies
      run: |
        python -m venv venv
        . venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        pip install black flake8 pytest
  ```

- **Run tests**: Activates the virtual environment and runs tests using `pytest`.
  ```yaml
    - name: Run tests
      run: |
        . venv/bin/activate
        pytest
  ```

---

### **Build and Push to ECR Workflow**

#### Overview
This workflow builds a Docker image and pushes it to Amazon ECR, ensuring the image is only pushed if the preceding "Test and Lint" workflow succeeds. The workflow is manually triggered using `workflow_dispatch` and depends on the completion of the "Test and Lint" workflow.

#### Workflow File Breakdown

**name**: Specifies the name of the workflow.
```yaml
name: Build and Push to ECR
```

**on**: Defines the event that triggers the workflow. `workflow_run` triggers this workflow after the "Test and Lint" workflow completes.
```yaml
on:
  workflow_run:
    workflows:
      - Test and Lint
    types:
      - completed
```

**jobs**: Defines the `build_and_push_to_ecr` job that runs on an Ubuntu runner, with a conditional to run only if the "Test and Lint" workflow succeeded.
```yaml
jobs:
  build_and_push_to_ecr:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
```

**steps**: Outlines the steps to build and push the Docker image.

- **Checkout code**: Uses `actions/checkout@v2` to pull the latest code.
  ```yaml
  steps:
    - name: Checkout code
      uses: actions/checkout@v2
  ```

- **Set up QEMU**: Uses `docker/setup-qemu-action@v2` for cross-platform builds.
  ```yaml
    - name: Set up QEMU
      uses: docker/setup-qemu-action@v2
  ```

- **Set up Docker Buildx**: Uses `docker/setup-buildx-action@v2` for advanced Docker build capabilities.
  ```yaml
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
  ```

- **Install AWS CLI**: Installs the AWS CLI to interact with Amazon services.
  ```yaml
    - name: Install AWS CLI
      run: |
        sudo apt-get update
        sudo apt-get install -y awscli
  ```

- **Log in to Amazon ECR**: Logs in to Amazon ECR using AWS credentials stored in GitHub Secrets.
  ```yaml
    - name: Log in to Amazon ECR
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        AWS_REGION: us-east-2
      run: |
        aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin 609324725328.dkr.ecr.us-east-2.amazonaws.com
  ```

- **Build and push Docker image to Amazon ECR**: Builds the Docker image and pushes it to the specified ECR repository.
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

---

By following these workflows, your project ensures that all code changes are rigorously tested and linted before building Docker images. These images are then securely pushed to Amazon ECR, streamlining your CI/CD pipeline and maintaining high standards for code quality and deployment.
