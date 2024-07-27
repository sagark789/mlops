import os
import joblib
import shutil
import pytest
from train import main, argparse
from sklearn.ensemble import RandomForestClassifier


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
        model_columns, RandomForestClassifier
    ), "The model is not a RandomForestClassifier."
