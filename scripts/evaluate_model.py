import os
import pickle
import json
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, mean_squared_error, r2_score

def load_model(model_path):
    """
    Load the machine learning model from a pickle file.
    """
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def load_data(data_path, target_column):
    """
    Load the dataset from a CSV file.
    """
    data = pd.read_csv(data_path)
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return X, y

def evaluate_classification_model(model, X, y):
    """
    Evaluate a classification model and print performance metrics.
    """
    predictions = model.predict(X)
    
    accuracy = accuracy_score(y, predictions)
    precision = precision_score(y, predictions, average='weighted')
    recall = recall_score(y, predictions, average='weighted')
    f1 = f1_score(y, predictions, average='weighted')
    conf_matrix = confusion_matrix(y, predictions)
    
    print("Classification Model Evaluation:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print("Confusion Matrix:")
    print(conf_matrix)
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': conf_matrix.tolist()
    }

def evaluate_regression_model(model, X, y):
    """
    Evaluate a regression model and print performance metrics.
    """
    predictions = model.predict(X)
    
    mse = mean_squared_error(y, predictions)
    r2 = r2_score(y, predictions)
    
    print("Regression Model Evaluation:")
    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"R^2 Score: {r2:.4f}")
    
    return {
        'mse': mse,
        'r2_score': r2
    }

def save_evaluation_results(results, output_path):
    """
    Save the evaluation results to a JSON file.
    """
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"Evaluation results saved to {output_path}")

def main(model_path, data_path, target_column, output_path, model_type):
    # Load the model and data
    model = load_model(model_path)
    X, y = load_data(data_path, target_column)
    
    # Evaluate the model
    if model_type == 'classification':
        results = evaluate_classification_model(model, X, y)
    elif model_type == 'regression':
        results = evaluate_regression_model(model, X, y)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Save the evaluation results
    save_evaluation_results(results, output_path)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate a machine learning model.")
    parser.add_argument('--model', type=str, required=True, help="Path to the trained model file (pickle format).")
    parser.add_argument('--data', type=str, required=True, help="Path to the dataset CSV file.")
    parser.add_argument('--target', type=str, required=True, help="The name of the target column in the dataset.")
    parser.add_argument('--output', type=str, required=True, help="Path to save the evaluation results (JSON format).")
    parser.add_argument('--model_type', type=str, required=True, choices=['classification', 'regression'], help="Type of the model: 'classification' or 'regression'.")
    
    args = parser.parse_args()
    main(args.model, args.data, args.target, args.output, args.model_type)
