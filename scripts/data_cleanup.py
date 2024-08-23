import os
import pandas as pd
import numpy as np
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
        - "mode": Fill with mode of the column.
        - "constant": Fill with a constant value specified by `fill_value`.
    fill_value: default=None
        The value to fill missing values with when strategy="constant".
    """
    if strategy == "mean":
        df = df.fillna(df.mean())
    elif strategy == "median":
        df = df.fillna(df.median())
    elif strategy == "mode":
        df = df.fillna(df.mode().iloc[0])
    elif strategy == "constant":
        if fill_value is not None:
            df = df.fillna(fill_value)
        else:
            raise ValueError("fill_value must be specified when strategy='constant'")
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
    
    return df

def remove_duplicates(df):
    """
    Remove duplicate rows from the dataset.
    """
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]
    print(f"Removed {before - after} duplicate rows.")
    return df

def standardize_data(df, columns):
    """
    Standardize the data format in specified columns.
    
    columns: list of str
        List of columns to standardize. For example, date columns or categorical columns.
    """
    for column in columns:
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            df[column] = pd.to_datetime(df[column])
        elif pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].astype(float)
        elif pd.api.types.is_categorical_dtype(df[column]) or df[column].dtype == 'object':
            df[column] = df[column].str.strip().str.lower()
    return df

def handle_outliers(df, method="IQR", threshold=1.5):
    """
    Handle outliers in the dataset.
    
    method: str, default="IQR"
        The method to use for outlier detection. Options:
        - "IQR": Use the interquartile range method to detect outliers.
        - "zscore": Use z-scores to detect outliers.
    threshold: float, default=1.5
        The threshold to use for outlier detection.
    """
    if method == "IQR":
        Q1 = df.quantile(0.25)
        Q3 = df.quantile(0.75)
        IQR = Q3 - Q1
        df = df[~((df < (Q1 - threshold * IQR)) | (df > (Q3 + threshold * IQR))).any(axis=1)]
    elif method == "zscore":
        from scipy.stats import zscore
        df = df[(np.abs(zscore(df.select_dtypes(include=[np.number]))) < threshold).all(axis=1)]
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return df

def save_clean_data(df, output_path):
    """
    Save the cleaned dataset to a CSV file.
    """
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

def main(input_file, output_file, strategy, fill_value, outlier_method, outlier_threshold):
    # Load the data
    df = load_data(input_file)

    # Handle missing values
    df = handle_missing_values(df, strategy=strategy, fill_value=fill_value)

    # Remove duplicates
    df = remove_duplicates(df)

    # Standardize data formats (example for standardizing all object-type columns)
    df = standardize_data(df, columns=df.select_dtypes(include=['object']).columns)

    # Handle outliers
    df = handle_outliers(df, method=outlier_method, threshold=outlier_threshold)

    # Save the cleaned data
    save_clean_data(df, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and preprocess a dataset.")
    parser.add_argument("input_file", type=str, help="Path to the input CSV file")
    parser.add_argument("output_file", type=str, help="Path to save the cleaned CSV file")
    parser.add_argument("--strategy", type=str, default="mean", choices=["mean", "median", "mode", "constant"],
                        help="Strategy for handling missing values")
    parser.add_argument("--fill_value", type=float, default=None,
                        help="Value to fill missing values when strategy is 'constant'")
    parser.add_argument("--outlier_method", type=str, default="IQR", choices=["IQR", "zscore"],
                        help="Method to handle outliers")
    parser.add_argument("--outlier_threshold", type=float, default=1.5,
                        help="Threshold for outlier detection")

    args = parser.parse_args()
    main(args.input_file, args.output_file, args.strategy, args.fill_value, args.outlier_method, args.outlier_threshold)
