FROM python:3.8-slim

# Install dependencies
RUN pip install --upgrade pip
RUN pip install sagemaker scikit-learn pandas

# Copy your training and inference scripts
COPY scripts/train.py /opt/ml/code/train.py
COPY scripts/inference.py /opt/ml/code/inference.py

# Set environment variables
ENV SAGEMAKER_PROGRAM train.py

# Entry point
ENTRYPOINT ["sh", "-c", "python /opt/ml/code/$SAGEMAKER_PROGRAM"]