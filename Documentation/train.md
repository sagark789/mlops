# train.py Explanation

This section provides an explanation of the `train.py` script, which is used for training a machine learning model. The script includes data preprocessing, model training, validation, and saving the trained model.

## Overview

The `train.py` script performs the following key tasks:
1. Loads and preprocesses training data.
2. Trains a `RandomForestClassifier` model.
3. Validates the model and prints the validation accuracy.
4. Saves the trained model to a specified directory.

### Script Breakdown

- Imports necessary libraries and suppresses warnings.
```python
import argparse
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")
```



- Constructs paths based on environment and loads the training data.
```python
def main(args):
    # Load training data
    train_data_path = os.path.join(args.train, "train.csv")
    output_dir = "/opt/ml/model"

    environment = os.getenv("ENVIRONMENT", "local")

    if environment == "local":
        train_data_path = "data/train/train.csv"
        output_dir = "output"

    data = pd.read_csv(train_data_path)
```

- Handles missing values, converts categorical variables, and drops unnecessary columns.
```python
    # Preprocess data (example for Titanic dataset)
    # Handle missing values
    data["Age"].fillna(data["Age"].median(), inplace=True)
    data["Embarked"].fillna(data["Embarked"].mode()[0], inplace=True)
    data["Fare"].fillna(data["Fare"].median(), inplace=True)
    data["Cabin"].fillna("U", inplace=True)
    data["Cabin"] = data["Cabin"].map(lambda x: x[0])

    # Convert categorical variables to dummy variables
    data = pd.get_dummies(data, columns=["Sex", "Embarked", "Cabin"], drop_first=True)

    # Drop unnecessary columns
    data.drop(["Name", "Ticket", "PassengerId"], axis=1, inplace=True)
```


- Defines features and target, and splits data into training and validation sets.
```python
    # Define features and target
    X = data.drop("Survived", axis=1)
    y = data["Survived"]

    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
```


- Trains the model, makes predictions on validation data, and prints the accuracy.
```python
    # Train model
    model = RandomForestClassifier(n_estimators=args.n_estimators)
    model.fit(X_train, y_train)

    # Validate model
    predictions = model.predict(X_val)
    accuracy = accuracy_score(y_val, predictions)

    print(f"Validation Accuracy: {accuracy}")
```

- Saves the trained model to the specified directory.
```python
    # Save model
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    model_path = os.path.join(output_dir, "model.joblib")
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
```


- Parses command-line arguments and calls the `main` function with the parsed arguments.
```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=str, help="Path to the training data", default="/opt/ml/input/data/train")
    parser.add_argument("--n-estimators", type=int, default=100)

    args = parser.parse_args()
    main(args)
```
