import os
import shutil
import json
import datetime
import pickle
import argparse

# Define a function to save a model backup
def backup_model(model, model_name, backup_dir='model_backups', metadata=None):
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f"{model_name}_{timestamp}")
    os.makedirs(backup_path, exist_ok=True)
    
    # Save the model
    model_file = os.path.join(backup_path, f"{model_name}.pkl")
    with open(model_file, 'wb') as f:
        pickle.dump(model, f)
    
    # Save the metadata
    metadata_file = os.path.join(backup_path, f"{model_name}_metadata.json")
    if metadata is None:
        metadata = {}
    metadata['backup_timestamp'] = timestamp
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f)
    
    print(f"Model and metadata backed up to: {backup_path}")
    return backup_path

# Define a function to restore a model from a backup
def restore_model(backup_path):
    # Load the model
    model_file = [f for f in os.listdir(backup_path) if f.endswith('.pkl')][0]
    with open(os.path.join(backup_path, model_file), 'rb') as f:
        model = pickle.load(f)
    
    # Load the metadata
    metadata_file = [f for f in os.listdir(backup_path) if f.endswith('_metadata.json')][0]
    with open(os.path.join(backup_path, metadata_file), 'r') as f:
        metadata = json.load(f)
    
    print(f"Model restored from backup: {backup_path}")
    return model, metadata

# Define a function to list available backups
def list_backups(backup_dir='model_backups'):
    backups = []
    if os.path.exists(backup_dir):
        for folder in os.listdir(backup_dir):
            folder_path = os.path.join(backup_dir, folder)
            if os.path.isdir(folder_path):
                backups.append(folder_path)
    else:
        print(f"No backup directory found: {backup_dir}")
    
    if backups:
        print("Available backups:")
        for backup in backups:
            print(f"- {backup}")
    else:
        print("No backups found.")

# Define a function to delete old backups
def delete_old_backups(backup_dir='model_backups', keep_last_n=5):
    if os.path.exists(backup_dir):
        backups = sorted(os.listdir(backup_dir), reverse=True)
        for backup in backups[keep_last_n:]:
            shutil.rmtree(os.path.join(backup_dir, backup))
            print(f"Deleted old backup: {backup}")
    else:
        print(f"No backup directory found: {backup_dir}")

# Main function for command-line interface
def main():
    parser = argparse.ArgumentParser(description="Backup and restore machine learning models.")
    parser.add_argument('action', choices=['backup', 'restore', 'list', 'delete_old'], help="Action to perform")
    parser.add_argument('--model', type=str, help="Path to the model file for backup or restore")
    parser.add_argument('--model_name', type=str, help="Name of the model for backup")
    parser.add_argument('--backup_dir', type=str, default='model_backups', help="Directory to store or retrieve backups")
    parser.add_argument('--metadata', type=str, help="Path to a JSON file containing model metadata")
    parser.add_argument('--keep_last_n', type=int, default=5, help="Number of recent backups to keep when deleting old ones")
    parser.add_argument('--backup_path', type=str, help="Path to the specific backup to restore")
    
    args = parser.parse_args()
    
    if args.action == 'backup':
        if args.model_name is None or args.model is None:
            parser.error("--model_name and --model are required for backup.")
        with open(args.model, 'rb') as f:
            model = pickle.load(f)
        metadata = {}
        if args.metadata:
            with open(args.metadata, 'r') as f:
                metadata = json.load(f)
        backup_model(model, args.model_name, backup_dir=args.backup_dir, metadata=metadata)
    
    elif args.action == 'restore':
        if args.backup_path is None:
            parser.error("--backup_path is required for restore.")
        model, metadata = restore_model(args.backup_path)
        print(f"Model: {model}")
        print(f"Metadata: {metadata}")
    
    elif args.action == 'list':
        list_backups(backup_dir=args.backup_dir)
    
    elif args.action == 'delete_old':
        delete_old_backups(backup_dir=args.backup_dir, keep_last_n=args.keep_last_n)

if __name__ == "__main__":
    main()
