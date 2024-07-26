import subprocess
import argparse
import boto3
import datetime
import os

def start_transform_job():
    # Set up client
    sagemaker_client = boto3.client('sagemaker')

    # Define model configuration
    model_name = 'titanic-model'
    region = "us-east-2"
    role_arn = "arn:aws:iam::609324725328:role/sagemaker-maven"
    ecr_image = "609324725328.dkr.ecr.us-east-2.amazonaws.com/maven_mlops_test"
    model_data_url = 's3://maven-mlops/output/custom-training-job-20240716230756/output/model.tar.gz'

    # Define transform job configuration
    transform_job_name = 'titanic-transform-job'
    input_location = "s3://maven-mlops/data/train"
    output_location = "s3://maven-mlops/output"

    # Create transform job
    response = sagemaker_client.create_transform_job(
        TransformJobName=transform_job_name,
        ModelName=model_name,
        MaxConcurrentTransforms=1,
        MaxPayloadInMB=6,
        BatchStrategy='SingleRecord',
        TransformOutput={
            'S3OutputPath': output_location,
            'AssembleWith': 'Line',  # Combines output into a single file
            'Accept': 'text/csv' 
        },
        TransformInput={
            'DataSource': {
                'S3DataSource': {
                    'S3DataType': 'S3Prefix',
                    'S3Uri': input_location,
                }
            },
            'ContentType': 'text/csv',
            'SplitType': 'Line'
        },
        TransformResources={
            'InstanceType': 'ml.m5.large',
            'InstanceCount': 1
        }
    )

    print(f"CreateTransformJob response: {response}")

def register_model():
    # Set up client
    sagemaker_client = boto3.client('sagemaker')

    # Define model configuration
    model_name = 'titanic-model'
    region = "us-east-2"
    role_arn = "arn:aws:iam::609324725328:role/sagemaker-maven"
    ecr_image = "609324725328.dkr.ecr.us-east-2.amazonaws.com/maven_mlops_test"
    model_data_url = 's3://maven-mlops/output/custom-training-job-20240716230756/output/model.tar.gz'

    response = sagemaker_client.create_model(
        ModelName=model_name,
        PrimaryContainer={
            'Image': ecr_image,
            'ModelDataUrl': model_data_url,
            'Environment': {
                # Add any environment variables your model needs for inference
                'SAGEMAKER_PROGRAM': 'inference.py',  # Assuming your entry point is named inference.py
            }
        },
        ExecutionRoleArn=role_arn,
        Tags=[
            {
                'Key': 'Project',
                'Value': 'TitanicPrediction'
            },
        ]
    )

    print(f"Model '{model_name}' created with ARN: {response['ModelArn']}")


def start_training_job():
    # Define AWS credentials and region
    region = "us-east-2"
    role_arn = "arn:aws:iam::609324725328:role/sagemaker-maven"

    # Define ECR image and S3 paths
    ecr_image = "609324725328.dkr.ecr.us-east-2.amazonaws.com/maven_mlops_test"
    s3_input_train = "s3://maven-mlops/data/train"
    s3_output_path = "s3://maven-mlops/output"

    # Initialize Boto3 SageMaker client
    sagemaker_client = boto3.client("sagemaker", region_name=region)

    # Define training job name
    training_job_name = (
        f'custom-training-job-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}'
    )

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

    # Create the training job
    response = sagemaker_client.create_training_job(**training_job_config)

    # Print the response
    print(response)

def main():
    parser = argparse.ArgumentParser(description='Orchestrate SageMaker Training and Inference')
    parser.add_argument('--mode', type=str, choices=['train', 'inference', 'register'], required=True,
                        help='Mode to run the orchestrator: train or inference')
    args = parser.parse_args()

    if args.mode == 'train':
        start_training_job()
    elif args.mode == 'inference':
        start_transform_job()
    elif args.mode == 'register':
        register_model()

if __name__ == "__main__":
    main()