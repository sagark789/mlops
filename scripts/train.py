import argparse
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def main():
    parser = argparse.ArgumentParser()
    
    # Input and output directories
    parser.add_argument('--train', type=str, default='/opt/ml/input/data/train')
    parser.add_argument('--model-dir', type=str, default='/opt/ml/model')
    
    args = parser.parse_args()
    
    # Load training data
    train_data = pd.read_csv(os.path.join(args.train, 'train.csv'))
    features = ["Pclass", "Sex", "SibSp", "Parch"]
    X_train = pd.get_dummies(train_data[features])
    y_train = train_data['Survived']
    
    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    
    # Save model
    joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))
    
if __name__ == '__main__':
    main()