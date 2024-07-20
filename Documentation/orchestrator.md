
# SageMaker Training Job Script Explanation

This section provides an explanation of the Python script, which is used to create and start a SageMaker training job using the Boto3 library. The script sets up the necessary configurations, including AWS credentials, ECR image, and S3 paths.

## Overview

The script performs the following key tasks:
1. Defines AWS credentials and region.
2. Defines ECR image and S3 paths for input and output data.
3. Initializes the Boto3 SageMaker client.
4. Configures the training job settings.
5. Creates and starts the SageMaker training job.

### Script Breakdown


- Imports the necessary libraries: `boto3` for AWS interactions and `datetime` for generating a unique training job name.

```python
import boto3
import datetime
```

- **region**: Specifies the AWS region.
- **role_arn**: Specifies the ARN of the IAM role with permissions to run the SageMaker job.

```python
# Define AWS credentials and region
region = "us-east-2"
role_arn = "arn:aws:iam::609324725328:role/sagemaker-maven"
```



- **ecr_image**: Specifies the URI of the Docker image in ECR.
- **s3_input_train**: Specifies the S3 path for the input training data.
- **s3_output_path**: Specifies the S3 path for the output data.
```python
# Define ECR image and S3 paths
ecr_image = "609324725328.dkr.ecr.us-east-2.amazonaws.com/maven_mlops_test"
s3_input_train = "s3://maven-mlops/data/train"
s3_output_path = "s3://maven-mlops/output"
```

- Initializes the SageMaker client using Boto3.
```python
# Initialize Boto3 SageMaker client
sagemaker_client = boto3.client("sagemaker", region_name=region)
```



- Generates a unique training job name using the current date and time.

```python
# Define training job name
training_job_name = (
    f'custom-training-job-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}'
)
```

- **TrainingJobName**: Specifies the name of the training job.
- **AlgorithmSpecification**: Defines the Docker image and input mode.
- **RoleArn**: Specifies the IAM role ARN.
- **InputDataConfig**: Configures the input data channel with S3 URI and content type.
- **OutputDataConfig**: Specifies the S3 path for output data.
- **ResourceConfig**: Defines the instance type, count, and volume size.
- **StoppingCondition**: Sets the maximum runtime for the training job.
- **HyperParameters**: Specifies hyperparameters for the training job.

```python
# Create training job configuration
training_job_config = {
    "TrainingJobName": training_job_name,
    "AlgorithmSpecification": {"TrainingImage": ecr_image, "TrainingInputMode": "File"},
    "RoleArn": role_arn,
    "InputDataConfig": [
        {
            "ChannelName": "train",
            "DataSource": {
                "S3DataSource": {
                    "S3DataType": "S3Prefix",
                    "S3Uri": s3_input_train,
                    "S3DataDistributionType": "FullyReplicated",
                }
            },
            "ContentType": "text/csv",
            "InputMode": "File",
        }
    ],
    "OutputDataConfig": {"S3OutputPath": s3_output_path},
    "ResourceConfig": {
        "InstanceType": "ml.m5.large",
        "InstanceCount": 1,
        "VolumeSizeInGB": 50,
    },
    "StoppingCondition": {"MaxRuntimeInSeconds": 3600},
    "HyperParameters": {"n_estimators": "100"},
}
```



- Creates the SageMaker training job using the configured settings.

```python
# Create the training job
response = sagemaker_client.create_training_job(**training_job_config)
```

