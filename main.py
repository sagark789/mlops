import os
from sagemaker.local import LocalSession
from sagemaker.session import Session
from sagemaker.estimator import Estimator

def get_sagemaker_session(deployment_type):
    if deployment_type == 'local':
        local_session = LocalSession()
        local_session.config = {'local': {'local_code': True}}
        return local_session
    elif deployment_type == 'cloud':
        return Session()
    else:
        raise ValueError("Deployment type not supported")

def main():
    deployment_type = os.getenv('DEPLOYMENT_TYPE', 'local')
    sagemaker_session = get_sagemaker_session(deployment_type)

    image_uri = 'public.ecr.aws/f3l2h4y6/mlops:latest'
    if deployment_type == 'local':
        role = 'arn:aws:iam::123456789012:role/DummyRoleForLocal'  # Dummy role ARN for local mode
        # Placeholder role for local mode
        instance_type = 'local'
        output_path = 'file://./output'
        train_data_path = 'file://./data/'
    else:
        role = os.getenv('SAGEMAKER_ROLE', 'arn:aws:iam::<your-account-id>:role/<your-sagemaker-role>')  # Replace with your actual SageMaker role ARN
        instance_type = 'ml.m5.large'
        output_path = 's3://<your-bucket>/output'
        train_data_path = 's3://<your-bucket>/data/train'

    estimator = Estimator(
        image_uri=image_uri,
        role=role,
        instance_count=1,
        instance_type=instance_type,
        output_path=output_path,
        sagemaker_session=sagemaker_session,
        environment={'SAGEMAKER_PROGRAM': 'train.py'}  # Change this to your actual script
    )

    estimator.fit({'train': train_data_path})

if __name__ == '__main__':
    main()
