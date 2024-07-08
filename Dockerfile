FROM python:3.8-slim

# Copy the hello_world script
COPY ../scripts/train.py /opt/ml/code/train.py

# Set environment variables
ENV SAGEMAKER_PROGRAM train.py

# Entry point
ENTRYPOINT ["sh", "-c", "python /opt/ml/code/$SAGEMAKER_PROGRAM"]
