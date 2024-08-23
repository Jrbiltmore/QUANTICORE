import os
import json
import pickle
import argparse
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR

def load_data(file_path):
    """
    Load the dataset from a CSV file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return pd.read_csv(file_path)

def preprocess_data(df, target_column, scale_features=True, encode_labels=True):
    """
    Preprocess the dataset: encode labels, scale features, and split into X and y.
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]

    if encode_labels and y.dtype == 'object':
        le = LabelEncoder()
        y = le.fit_transform(y)

    if scale_features:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
    
    return X, y

def train_model(X_train, y_train, model_type='classification', model_name='random_forest'):
    """
    Train a machine learning model.
    """
    if model_type == 'classification':
        if model_name == 'random_forest':
            model = RandomForestClassifier()
        elif model_name == 'logistic_regression':
            model = LogisticRegression()
        elif model_name == 'svm':
            model = SVC()
        else:
            raise ValueError(f"Unknown model name: {model_name}")
    elif model_type == 'regression':
        if model_name == 'random_forest':
            model = RandomForestRegressor()
        elif model_name == 'linear_regression':
            model = LinearRegression()
        elif model_name == 'svm':
            model = SVR()
        else:
            raise ValueError(f"Unknown model name: {model_name}")
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test, model_type='classification'):
    """
    Evaluate the model on the test set and return performance metrics.
    """
    predictions = model.predict(X_test)

    if model_type == 'classification':
        accuracy = accuracy_score(y_test, predictions)
        return {'accuracy': accuracy}
    elif model_type == 'regression':
        mse = mean_squared_error(y_test, predictions)
        return {'mse': mse}
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def save_model(model, output_dir, model_name='model'):
    """
    Save the trained model and metadata to the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    model_path = os.path.join(output_dir, f'{model_name}.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    metadata = {
        'model_name': model_name,
        'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'model_params': model.get_params()
    }
    
    metadata_path = os.path.join(output_dir, f'{model_name}_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)

    print(f"Model and metadata saved to {output_dir}")

def main(input_file, target_column, model_type, model_name, test_size, output_dir, scale_features, encode_labels):
    # Load and preprocess data
    df = load_data(input_file)
    X, y = preprocess_data(df, target_column, scale_features=scale_features, encode_labels=encode_labels)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    # Train the model
    model = train_model(X_train, y_train, model_type=model_type, model_name=model_name)

    # Evaluate the model
    performance = evaluate_model(model, X_test, y_test, model_type=model_type)
    print(f"Model Performance: {performance}")

    # Save the model and metadata
    save_model(model, output_dir, model_name=model_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a machine learning model.")
    parser.add_argument('--input_file', type=str, required=True, help="Path to the input CSV file containing the dataset.")
    parser.add_argument('--target_column', type=str, required=True, help="The name of the target column in the dataset.")
    parser.add_argument('--model_type', type=str, required=True, choices=['classification', 'regression'], help="Type of model to train.")
    parser.add_argument('--model_name', type=str, default='random_forest', help="The name of the model to train (e.g., 'random_forest', 'logistic_regression', 'svm').")
    parser.add_argument('--test_size', type=float, default=0.2, help="Proportion of the dataset to include in the test split.")
    parser.add_argument('--output_dir', type=str, required=True, help="Directory to save the trained model and metadata.")
    parser.add_argument('--scale_features', action='store_true', help="Scale numerical features before training.")
    parser.add_argument('--encode_labels', action='store_true', help="Encode target labels if they are categorical.")
    
    args = parser.parse_args()
    main(args.input_file, args.target_column, args.model_type, args.model_name, args.test_size, args.output_dir, args.scale_features, args.encode_labels)
