import os
import pickle
import json
import argparse

def load_model(model_path):
    """
    Load the machine learning model from a pickle file.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    return model

def load_metadata(metadata_path):
    """
    Load the model metadata from a JSON file.
    """
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    return metadata

def verify_backup(model_path, metadata_path):
    """
    Verify the integrity of the backup by checking if both model and metadata files exist.
    """
    if not os.path.exists(model_path):
        return False, f"Model file missing: {model_path}"
    
    if not os.path.exists(metadata_path):
        return False, f"Metadata file missing: {metadata_path}"
    
    return True, "Backup integrity verified."

def restore_model(backup_dir, verbose=False):
    """
    Restore the model and metadata from the backup directory.
    """
    model_path = os.path.join(backup_dir, 'model.pkl')
    metadata_path = os.path.join(backup_dir, 'metadata.json')
    
    # Verify the backup
    is_valid, message = verify_backup(model_path, metadata_path)
    if not is_valid:
        raise FileNotFoundError(message)
    
    # Load the model and metadata
    model = load_model(model_path)
    metadata = load_metadata(metadata_path)
    
    if verbose:
        print("Model and metadata successfully restored.")
        print(f"Model details: {metadata.get('model_name', 'Unknown Model')}")
        print(f"Training date: {metadata.get('training_date', 'Unknown')}")
        print(f"Performance: {metadata.get('performance', 'Not available')}")
    
    return model, metadata

def main(backup_dir, verbose):
    try:
        model, metadata = restore_model(backup_dir, verbose)
        print("Model restored successfully.")
        
        if verbose:
            print("Model parameters:")
            print(model.get_params() if hasattr(model, 'get_params') else "Model does not have parameters info.")
        
    except Exception as e:
        print(f"Failed to restore model: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Restore a machine learning model from a backup.")
    parser.add_argument('--backup_dir', type=str, required=True, help="Path to the backup directory containing the model and metadata.")
    parser.add_argument('--verbose', action='store_true', help="Print detailed information about the restored model.")
    
    args = parser.parse_args()
    main(args.backup_dir, args.verbose)
