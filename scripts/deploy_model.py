import os
import pickle
import json
from flask import Flask, request, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Load the model and metadata
def load_model(model_path, metadata_path=None):
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    metadata = {}
    if metadata_path and os.path.exists(metadata_path):
        with open(metadata_path, 'r') as meta_file:
            metadata = json.load(meta_file)
    return model, metadata

# Define the predict route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the JSON data from the request
        data = request.get_json(force=True)
        
        # Convert the JSON data into a format suitable for the model
        features = [data.get(key) for key in metadata['feature_names']]
        prediction = model.predict([features])
        
        # Return the prediction as a JSON response
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Define the health check route
@app.route('/health', methods=['GET'])
def health_check():
    try:
        return jsonify({'status': 'healthy', 'model_name': metadata.get('model_name', 'Unknown')}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

# Main function to start the Flask app
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Deploy a machine learning model using Flask.")
    parser.add_argument('--model', type=str, required=True, help="Path to the trained model file (pickle format).")
    parser.add_argument('--metadata', type=str, help="Path to the model metadata JSON file.")
    parser.add_argument('--host', type=str, default='0.0.0.0', help="Host to run the Flask app on.")
    parser.add_argument('--port', type=int, default=5000, help="Port to run the Flask app on.")
    
    args = parser.parse_args()

    # Load the model and metadata
    model, metadata = load_model(args.model, args.metadata)

    # Start the Flask app
    app.run(host=args.host, port=args.port)
