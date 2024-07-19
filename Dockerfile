FROM python:3.8-slim

# Install necessary libraries
RUN pip install pandas scikit-learn

# Set environment variables
ENV MODE="train"
ENV ENVIRONMENT="cloud"

# Copy your scripts
COPY train.py /opt/ml/code/train.py
COPY inference.py /opt/ml/code/inference.py 
COPY main.py /opt/ml/code/main.py

# Define the entry point for the container
ENTRYPOINT ["python", "/opt/ml/code/main.py"]