import argparse
import os
import pandas as pd
import joblib

def main():
    parser = argparse.ArgumentParser()
    
    # Input and output directories
    parser.add_argument('--model-dir', type=str, default='/opt/ml/model')
    parser.add_argument('--input', type=str, default='/opt/ml/input/data/test')
    parser.add_argument('--output', type=str, default='/opt/ml/output')
    
    args = parser.parse_args()
    
    # Load model
    model = joblib.load(os.path.join(args.model_dir, 'model.joblib'))
    
    # Load test data
    test_data = pd.read_csv(os.path.join(args.input, 'test.csv'))
    X_test = test_data.drop(['PassengerId'], axis=1)
    
    # Make predictions
    predictions = model.predict(X_test)
    
    # Save predictions
    output = pd.DataFrame({'PassengerId': test_data['PassengerId'], 'Survived': predictions})
    output.to_csv(os.path.join(args.output, 'predictions.csv'), index=False)
    
if __name__ == '__main__':
    main()
