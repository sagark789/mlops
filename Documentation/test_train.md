# README: Testing the Training Script (`test_train.py`)

This README provides an overview of the `test_train.py` script, which is designed to test the functionality of the `train.py` machine learning training script. The test script utilizes the `pytest` framework to automate the testing process, ensuring the training script runs correctly and produces the expected outputs.

## Overview

The `test_train.py` script contains unit tests for the `train.py` script, specifically focusing on verifying that the training process completes successfully and the model is saved correctly. The tests include setup and teardown procedures to ensure a clean testing environment, and they check the output model's type and existence.

## Test Script Breakdown

### Imports and Setup

```python
import os
import joblib
import shutil
import pytest
from train import main, argparse
from sklearn.ensemble import RandomForestClassifier
```

- **os, joblib, shutil**: Standard Python libraries for file and directory operations.
- **pytest**: Testing framework used for structuring and running tests.
- **train (main, argparse)**: Importing the `main` function and `argparse` module from the `train.py` script.
- **RandomForestClassifier**: The expected type of the trained model, imported for verification purposes.

### Fixture: `setup_and_teardown`

```python
@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup: Create sample data directory and file
    os.makedirs("test_data", exist_ok=True)
    sample_data = """PassengerId,Survived,Pclass,Name,Sex,Age,SibSp,Parch,Ticket,Fare,Cabin,Embarked
1,0,3,Braund, Mr. Owen Harris,male,22,1,0,A/5 21171,7.25,,S
2,1,1,Cumings, Mrs. John Bradley (Florence Briggs Thayer),female,38,1,0,PC 17599,71.2833,C85,C
3,1,3,Heikkinen, Miss. Laina,female,26,0,0,STON/O2. 3101282,7.925,,S
4,1,1,Futrelle, Mrs. Jacques Heath (Lily May Peel),female,35,1,0,113803,53.1,C123,S
5,0,3,Allen, Mr. William Henry,male,35,0,0,373450,8.05,,S
"""
    with open("test_data/train.csv", "w") as f:
        f.write(sample_data)

    yield  # This will run the test

    # Teardown: Remove sample data directory and output directory
    shutil.rmtree("test_data")
    if os.path.exists("output"):
        shutil.rmtree("output")
```

#### Description:
- **Setup**:
  - A temporary directory `test_data` is created, and a sample CSV file `train.csv` is written with sample data resembling the Titanic dataset. This data is used to test the training process.
- **Teardown**:
  - After the tests run, the `test_data` directory and any output files in the `output` directory are removed to clean up the environment, ensuring no residual data affects subsequent tests.

### Test Function: `test_train_script`

```python
def test_train_script():
    # Prepare arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=str, default="test_data")
    parser.add_argument(
        "--n-estimators", type=int, default=10
    )  # Use fewer estimators for quick testing
    args = parser.parse_args(args=[])

    # Run the training script
    main(args)

    # Check if the model file is created
    model_path = "output/model.joblib"
    assert os.path.exists(model_path), "Model file was not created."

    # Load the model and check if it's a RandomForestClassifier
    model, model_columns = joblib.load(model_path)
    
    assert isinstance(
        model, RandomForestClassifier
    ), "The model is not a RandomForestClassifier."
```

#### Description:
- **Argument Parsing**:
  - The test prepares mock command-line arguments for the training script, setting the training data path to `test_data` and reducing the number of estimators to 10 for quicker test execution.
- **Run Training Script**:
  - The `main` function from the `train.py` script is invoked with the test arguments, simulating the training process.
- **Assertions**:
  - The test checks if the model file `output/model.joblib` is created.
  - It then loads the saved model and verifies that it is an instance of `RandomForestClassifier`, ensuring the training script works as expected and produces a valid model.

## How to Run the Tests

1. **Install Dependencies**: Ensure you have `pytest` and other necessary dependencies installed.
   ```bash
   pip install pytest
   ```

2. **Run the Tests**: Use the following command to run the tests.
   ```bash
   pytest test_train.py
   ```

## Conclusion

The `test_train.py` script provides automated testing for the `train.py` script, ensuring that the model training process runs correctly and the output is as expected. This setup helps in maintaining the reliability and robustness of the machine learning pipeline.
