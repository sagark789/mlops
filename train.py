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

def main(args):
    # Load training data
    train_data_path = os.path.join(args.train, 'train.csv')
    output_dir = '/opt/ml/model'

    environment = os.getenv('ENVIRONMENT', 'local')

    if environment == 'local':
        train_data_path = 'data/train/train.csv'
        output_dir = 'output'

    data = pd.read_csv(train_data_path)
    
    # Preprocess data (example for Titanic dataset)
    # Handle missing values
    data['Age'].fillna(data['Age'].median(), inplace=True)
    data['Embarked'].fillna(data['Embarked'].mode()[0], inplace=True)
    data['Fare'].fillna(data['Fare'].median(), inplace=True)
    data['Cabin'].fillna('U', inplace=True)
    data['Cabin'] = data['Cabin'].map(lambda x: x[0])  # Use first letter of cabin

    # Convert categorical variables to dummy variables
    data = pd.get_dummies(data, columns=['Sex', 'Embarked', 'Cabin'], drop_first=True)
    
    # Drop unnecessary columns
    data.drop(['Name', 'Ticket', 'PassengerId'], axis=1, inplace=True)

    # Define features and target
    X = data.drop('Survived', axis=1)
    y = data['Survived']
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=args.n_estimators)
    model.fit(X_train, y_train)
    
    # Validate model
    predictions = model.predict(X_val)
    accuracy = accuracy_score(y_val, predictions)
    
    print(f'Validation Accuracy: {accuracy}')
    
    # Save model
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save model
    model_path = os.path.join(output_dir, 'model.joblib')
    joblib.dump(model, model_path)
    print(f'Model saved to {model_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', type=str, help='Path to the training data', default='/opt/ml/input/data/train')
    parser.add_argument('--n-estimators', type=int, default=100)
    
    args = parser.parse_args()
    main(args)
