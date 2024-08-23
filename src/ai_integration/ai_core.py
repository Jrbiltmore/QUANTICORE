import logging
import pickle
import os
from datetime import datetime

class AICore:
    def __init__(self, models_dir='models', log_file='ai_core.log'):
        """
        Initialize the AI Core with directories for storing models and logs.
        """
        self.models = {}
        self.models_dir = models_dir
        self.log_file = log_file
        self._setup_logging()

    def _setup_logging(self):
        """
        Set up logging for the AI Core.
        """
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("AI Core initialized")

    def load_model(self, model_name):
        """
        Load a model from the models directory.
        """
        model_path = os.path.join(self.models_dir, f'{model_name}.pkl')
        metadata_path = os.path.join(self.models_dir, f'{model_name}_metadata.json')

        if not os.path.exists(model_path):
            logging.error(f"Model {model_name} not found at {model_path}")
            raise FileNotFoundError(f"Model {model_name} not found.")
        
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
        
        with open(metadata_path, 'r') as metadata_file:
            metadata = json.load(metadata_file)
        
        self.models[model_name] = {
            'model': model,
            'metadata': metadata
        }
        logging.info(f"Model {model_name} loaded successfully.")

    def save_model(self, model, model_name, metadata=None):
        """
        Save a model to the models directory.
        """
        os.makedirs(self.models_dir, exist_ok=True)
        
        model_path = os.path.join(self.models_dir, f'{model_name}.pkl')
        metadata_path = os.path.join(self.models_dir, f'{model_name}_metadata.json')
        
        with open(model_path, 'wb') as model_file:
            pickle.dump(model, model_file)
        
        if metadata is None:
            metadata = {}
        
        metadata['model_name'] = model_name
        metadata['save_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(metadata_path, 'w') as metadata_file:
            json.dump(metadata, metadata_file, indent=4)
        
        logging.info(f"Model {model_name} saved successfully.")

    def predict(self, model_name, input_data):
        """
        Perform a prediction using the specified model.
        """
        if model_name not in self.models:
            logging.error(f"Model {model_name} is not loaded.")
            raise ValueError(f"Model {model_name} is not loaded.")
        
        model = self.models[model_name]['model']
        prediction = model.predict([input_data])
        logging.info(f"Prediction made using model {model_name}: {prediction}")
        return prediction

    def list_models(self):
        """
        List all models currently loaded in the AI Core.
        """
        return list(self.models.keys())

    def unload_model(self, model_name):
        """
        Unload a model from the AI Core.
        """
        if model_name in self.models:
            del self.models[model_name]
            logging.info(f"Model {model_name} unloaded successfully.")
        else:
            logging.error(f"Attempted to unload model {model_name}, but it is not loaded.")
            raise ValueError(f"Model {model_name} is not loaded.")

    def log_event(self, message, level='info'):
        """
        Log a custom event to the AI Core log file.
        """
        if level == 'info':
            logging.info(message)
        elif level == 'warning':
            logging.warning(message)
        elif level == 'error':
            logging.error(message)
        else:
            logging.info(message)
        print(f"Logged: {message}")

    def get_model_metadata(self, model_name):
        """
        Retrieve metadata for a specific model.
        """
        if model_name in self.models:
            return self.models[model_name]['metadata']
        else:
            logging.error(f"Requested metadata for model {model_name}, but it is not loaded.")
            raise ValueError(f"Model {model_name} is not loaded.")


# Example usage
if __name__ == "__main__":
    ai_core = AICore()

    # Load a model
    try:
        ai_core.load_model('example_model')
    except FileNotFoundError as e:
        ai_core.log_event(str(e), level='error')

    # Make a prediction
    try:
        input_data = [5.1, 3.5, 1.4, 0.2]  # Example input data
        prediction = ai_core.predict('example_model', input_data)
        print(f"Prediction: {prediction}")
    except ValueError as e:
        ai_core.log_event(str(e), level='error')

    # Save a model (as an example, saving the already loaded model)
    try:
        model = ai_core.models['example_model']['model']
        ai_core.save_model(model, 'example_model_v2')
    except KeyError as e:
        ai_core.log_event(str(e), level='error')

    # Unload the model
    try:
        ai_core.unload_model('example_model')
    except ValueError as e:
        ai_core.log_event(str(e), level='error')

    # List loaded models
    print("Loaded models:", ai_core.list_models())
