# Productionizing an ML Model

### 1. Initial Setup
1. **Create a GitHub Project:**
    - Create a new repository on GitHub.
    - Clone the repository to your local machine.
2. **Install GitHub Desktop:**
    - Download and install [GitHub Desktop](https://github.com/apps/desktop).
3. **Download and Setup VSCode:**
    - Download and install Visual Studio Code.
    - Open your project folder in VSCode.
    - Set up a virtual environment in VSCode.

### 2. AWS IAM Setup
1. **Create IAM User with Proper Permissions:**
    - Go to the IAM console in AWS.
    - Create a new IAM user with programmatic access.
    - Attach policies for Amazon S3, Amazon ECR, and Amazon SageMaker (e.g., `AmazonS3FullAccess`, `AmazonEC2ContainerRegistryFullAccess`, `AmazonSageMakerFullAccess`).
2. **Configure AWS CLI with IAM User Credentials:**
    - Install [**AWS CLI**](https://aws.amazon.com/cli/).
    - Run `aws configure` and input the IAM user’s access key, secret key, default region, and output format.

### 3. Project Structure
1. **Create Project Files and Folders:**
    - `main.py`: This is your main code that controls the entry into training and inference scripts:
    - `train.py`: Your main training script.
    - `requirements.txt`: List of dependencies.
    - `inference.py`: Your main inference script.
    - `data/`: Directory to store your dataset.
2. **Download Data from Kaggle:**
    - Download the dataset from [Kaggle](https://www.kaggle.com/competitions/titanic/data).
    - Place the dataset in the `data/` folder.
3. Create a virtual environment
4. **Install Dependencies:**
    - Install the dependencies listed in `requirements.txt` within your virtual environment.
5. **Run the Training Script using launch.json (via main.py)**

### 4. Dockerization
1. **Install Docker:**
    - Download and install Docker.
2. **Create Dockerfile:**
    - Write a Dockerfile to containerize your application.
3. **Build and Run Docker Image:**
    - Build the Docker image.
    - Run the Docker container and verify the results.
      `docker run -v $(pwd)/data:/opt/ml/input/data -v $(pwd)/output:/opt/ml/output -v $(pwd)/model:/opt/ml/model my_mlops_image --mode train`

### 5. S3 Integration [Optional]
1. **Upload Data to S3:**
    - Upload your dataset to an S3 bucket.
    - Ensure your IAM user has `s3:PutObject` and `s3:GetObject` permissions.
2. **Modify Code for S3 Integration:**
    - Update your code to download the data from S3 at runtime using Boto3.

### 6. Docker Image on ECR
1. **Setup ECR Repository:**
    - Create a repository on Amazon Elastic Container Registry (ECR).
2. **Push Docker Image to ECR:**
    - Authenticate Docker to your ECR using IAM credentials.
    - Tag and push your Docker image to ECR.
3. **Download Image from ECR [optional]:**
    - Pull the Docker image from ECR and run it locally to verify.

### 6. Writing Effective Test Cases
1. **Setup and Teardown**: 
   - Initialize any required data or environment before the test.
   - Clean up afterward to maintain test isolation and prevent interference between tests.
2. **Define the Test Scope**: 
   - Clearly specify the functionality or feature the test case covers.
   - Focus on specific inputs and expected outputs to ensure comprehensive testing.
3. **Assertions and Validation**: 
   - Use assertions to validate the expected outcomes.
   - Ensure the test checks for correct functionality and handles potential edge cases effectively.


### 7. GitHub Integration
1. **Get AWS Keys and Set Up in GitHub Configuration**
   - Obtain the necessary AWS access and secret keys.
   - Add these keys as secrets in your GitHub repository under "Settings" > "Secrets and variables" > "Actions".
2. **Create a Workflow to Run Tests**
   - Set up a GitHub Actions workflow that installs dependencies, runs tests, and reports the results.
3. **Create a Workflow to Build and Push the Image to ECR**
   - Define a GitHub Actions workflow to build a Docker image, tag it, and push it to Amazon ECR (Elastic Container Registry).


### 8. SageMaker Endpoint Integration

1. **Write the Inference Script and Test Locally**
   - Develop an inference script that handles data preprocessing, model prediction, and postprocessing.
   - Test the script locally to ensure it produces the correct outputs with the expected inputs.

2. **Register the Model**
   - Save the trained model in a format compatible with Amazon SageMaker.
   - Register the model with SageMaker, specifying the model artifact location and necessary configurations.

3. **Invoke the Batch Transformation**
   - Set up a SageMaker batch transformation job to process large datasets in batch mode.
   - Define the input and output locations, and configure the job parameters to suit your needs.



