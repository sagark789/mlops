import boto3

def main():
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



if __name__ == "__main__":
    main()