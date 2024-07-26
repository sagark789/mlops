import os
import joblib
import pandas as pd
import argparse

def preprocess_data(data, model_columns=None):
    # Handle missing values
    data["Age"].fillna(data["Age"].median(), inplace=True)
    data["Embarked"].fillna(data["Embarked"].mode()[0], inplace=True)
    data["Fare"].fillna(data["Fare"].median(), inplace=True)
    data["Cabin"].fillna("U", inplace=True)
    data["Cabin"] = data["Cabin"].map(lambda x: x[0])  # Use first letter of cabin

    # Convert categorical variables to dummy variables
    data = pd.get_dummies(data, columns=["Sex", "Embarked", "Cabin"], drop_first=True)

    # Drop unnecessary columns
    data.drop(["Name", "Ticket", "PassengerId"], axis=1, inplace=True)

    if model_columns is not None:
        # Add missing columns
        missing_cols = set(model_columns) - set(data.columns)
        for col in missing_cols:
            data[col] = 0
    
        # Ensure the order of columns matches the model's expectations
        data = data[model_columns]

    return data

def load_model(model_path):
    return joblib.load(model_path)

def main(args):
    environment = os.getenv("ENVIRONMENT", "local")
    test_data_path = os.path.join(args.inference, "test.csv")
    model_path = "/opt/ml/output/model.joblib"
    output_path = "/opt/ml/output/predictions.csv"

    if environment == "local":
        test_data_path = "data/test/test.csv"
        model_path = "output/model.joblib"
        output_path = "output/predictions.csv"

    # Load model
    # model = load_model(model_path)
    model, model_columns = joblib.load(model_path)
    print(model_columns)
    test_data = pd.read_csv(test_data_path)

    # test_data_processed = preprocess_data(test_data)
    test_data_processed = preprocess_data(test_data, model_columns=model_columns)

    predictions = model.predict(test_data_processed)

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    pd.DataFrame(predictions, columns=["Survived"]).to_csv(output_path, index=False)
    print(f"Predictions saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inference",
        type=str,
        help="Path to the inference data",
        default="/opt/ml/input/data/test",
    )
    parser.add_argument("--n-estimators", type=int, default=100)

    args = parser.parse_args()
    main(args)
