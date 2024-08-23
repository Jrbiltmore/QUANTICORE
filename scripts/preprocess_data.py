import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import argparse

def load_data(file_path):
    """
    Load the dataset from a CSV file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return pd.read_csv(file_path)

def handle_missing_values(df, strategy="mean", fill_value=None):
    """
    Handle missing values in the dataset.
    
    strategy: str, default="mean"
        The strategy to use for filling missing values. Options:
        - "mean": Fill with mean of the column.
        - "median": Fill with median of the column.
        - "most_frequent": Fill with most frequent value of the column.
        - "constant": Fill with a constant value specified by `fill_value`.
    fill_value: default=None
        The value to fill missing values with when strategy="constant".
    """
    if strategy not in ["mean", "median", "most_frequent", "constant"]:
        raise ValueError(f"Unknown strategy: {strategy}")
    
    imputer = SimpleImputer(strategy=strategy, fill_value=fill_value)
    return pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

def encode_categorical_features(df, categorical_columns):
    """
    Encode categorical variables using one-hot encoding.
    
    categorical_columns: list of str
        The list of categorical columns to encode.
    """
    encoder = OneHotEncoder(sparse=False, drop='first')
    encoded_data = encoder.fit_transform(df[categorical_columns])
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_columns))
    df = df.drop(columns=categorical_columns)
    df = pd.concat([df, encoded_df], axis=1)
    return df

def scale_features(df, scaling_strategy="standard"):
    """
    Scale numerical features using the specified strategy.
    
    scaling_strategy: str, default="standard"
        The strategy to use for scaling features. Options:
        - "standard": Standardize features by removing the mean and scaling to unit variance.
        - "minmax": Scale features to a range (default 0 to 1).
    """
    if scaling_strategy not in ["standard", "minmax"]:
        raise ValueError(f"Unknown scaling strategy: {scaling_strategy}")
    
    scaler = StandardScaler() if scaling_strategy == "standard" else MinMaxScaler()
    scaled_data = scaler.fit_transform(df)
    return pd.DataFrame(scaled_data, columns=df.columns)

def split_data(df, target_column, test_size=0.2, random_state=42):
    """
    Split the dataset into training and testing sets.
    
    target_column: str
        The name of the target column.
    test_size: float, default=0.2
        The proportion of the dataset to include in the test split.
    random_state: int, default=42
        The seed used by the random number generator.
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

def save_data(X_train, X_test, y_train, y_test, output_dir):
    """
    Save the preprocessed data to CSV files.
    
    output_dir: str
        The directory to save the output files.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    X_train.to_csv(os.path.join(output_dir, 'X_train.csv'), index=False)
    X_test.to_csv(os.path.join(output_dir, 'X_test.csv'), index=False)
    y_train.to_csv(os.path.join(output_dir, 'y_train.csv'), index=False)
    y_test.to_csv(os.path.join(output_dir, 'y_test.csv'), index=False)

    print(f"Preprocessed data saved to {output_dir}")

def main(input_file, target_column, output_dir, missing_strategy, fill_value, categorical_columns, scaling_strategy, test_size, random_state):
    # Load the data
    df = load_data(input_file)

    # Handle missing values
    df = handle_missing_values(df, strategy=missing_strategy, fill_value=fill_value)

    # Encode categorical features
    if categorical_columns:
        df = encode_categorical_features(df, categorical_columns)

    # Scale numerical features
    df = scale_features(df, scaling_strategy=scaling_strategy)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(df, target_column, test_size=test_size, random_state=random_state)

    # Save the preprocessed data
    save_data(X_train, X_test, y_train, y_test, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess a dataset for machine learning.")
    parser.add_argument('--input_file', type=str, required=True, help="Path to the input CSV file.")
    parser.add_argument('--target_column', type=str, required=True, help="Name of the target column.")
    parser.add_argument('--output_dir', type=str, required=True, help="Directory to save the preprocessed data.")
    parser.add_argument('--missing_strategy', type=str, default="mean", choices=["mean", "median", "most_frequent", "constant"],
                        help="Strategy for handling missing values.")
    parser.add_argument('--fill_value', type=float, default=None, help="Value to fill missing values when strategy is 'constant'.")
    parser.add_argument('--categorical_columns', type=str, nargs='+', help="List of categorical columns to encode.")
    parser.add_argument('--scaling_strategy', type=str, default="standard", choices=["standard", "minmax"],
                        help="Strategy for scaling numerical features.")
    parser.add_argument('--test_size', type=float, default=0.2, help="Proportion of the dataset to include in the test split.")
    parser.add_argument('--random_state', type=int, default=42, help="Seed used by the random number generator for splitting the data.")
    
    args = parser.parse_args()
    main(args.input_file, args.target_column, args.output_dir, args.missing_strategy, args.fill_value, args.categorical_columns, args.scaling_strategy, args.test_size, args.random_state)
