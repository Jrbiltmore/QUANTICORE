import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, r2_score, confusion_matrix, classification_report
import seaborn as sns

class ModelPerformance:
    def __init__(self, model, X_test, y_test, model_type='classification'):
        """
        Initialize the ModelPerformance class.

        :param model: Trained machine learning model
        :param X_test: Features from the test set
        :param y_test: True labels or target values from the test set
        :param model_type: Type of model ('classification' or 'regression')
        """
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
        self.model_type = model_type
        self.predictions = model.predict(X_test)

    def evaluate_classification(self):
        """
        Evaluate a classification model and return performance metrics.
        """
        accuracy = accuracy_score(self.y_test, self.predictions)
        precision = precision_score(self.y_test, self.predictions, average='weighted')
        recall = recall_score(self.y_test, self.predictions, average='weighted')
        f1 = f1_score(self.y_test, self.predictions, average='weighted')
        conf_matrix = confusion_matrix(self.y_test, self.predictions)
        class_report = classification_report(self.y_test, self.predictions)

        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': conf_matrix.tolist(),
            'classification_report': class_report
        }
        
        return metrics

    def evaluate_regression(self):
        """
        Evaluate a regression model and return performance metrics.
        """
        mse = mean_squared_error(self.y_test, self.predictions)
        r2 = r2_score(self.y_test, self.predictions)

        metrics = {
            'mean_squared_error': mse,
            'r2_score': r2
        }
        
        return metrics

    def evaluate(self):
        """
        Evaluate the model based on its type.
        """
        if self.model_type == 'classification':
            return self.evaluate_classification()
        elif self.model_type == 'regression':
            return self.evaluate_regression()
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

    def save_metrics(self, output_path):
        """
        Save the performance metrics to a JSON file.
        """
        metrics = self.evaluate()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(metrics, f, indent=4)
        print(f"Performance metrics saved to {output_path}")

    def plot_confusion_matrix(self, output_path=None):
        """
        Plot and optionally save the confusion matrix for classification models.
        """
        if self.model_type != 'classification':
            raise ValueError("Confusion matrix is only available for classification models.")
        
        conf_matrix = confusion_matrix(self.y_test, self.predictions)
        plt.figure(figsize=(8, 6))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=np.unique(self.y_test), yticklabels=np.unique(self.y_test))
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title('Confusion Matrix')
        
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            plt.savefig(output_path)
            print(f"Confusion matrix plot saved to {output_path}")
        
        plt.show()

    def plot_residuals(self, output_path=None):
        """
        Plot and optionally save the residuals for regression models.
        """
        if self.model_type != 'regression':
            raise ValueError("Residuals plot is only available for regression models.")
        
        residuals = self.y_test - self.predictions
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=self.predictions, y=residuals)
        plt.axhline(0, color='r', linestyle='--')
        plt.xlabel('Predicted Values')
        plt.ylabel('Residuals')
        plt.title('Residuals Plot')
        
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            plt.savefig(output_path)
            print(f"Residuals plot saved to {output_path}")
        
        plt.show()

# Example usage
if __name__ == "__main__":
    # Assume X_test, y_test are the test set data and 'model' is the trained machine learning model
    # model = some_trained_model
    # X_test = some_test_features
    # y_test = some_test_labels
    
    # For classification
    # performance = ModelPerformance(model, X_test, y_test, model_type='classification')
    
    # For regression
    # performance = ModelPerformance(model, X_test, y_test, model_type='regression')
    
    # Evaluate the model
    # metrics = performance.evaluate()
    # print(metrics)
    
    # Save the metrics
    # performance.save_metrics('output/model_performance.json')
    
    # Plot confusion matrix (only for classification)
    # performance.plot_confusion_matrix('output/confusion_matrix.png')
    
    # Plot residuals (only for regression)
    # performance.plot_residuals('output/residuals_plot.png')
    pass
