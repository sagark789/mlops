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

if __name__ == "__main__":
    main()