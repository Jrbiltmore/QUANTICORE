
import os

def save_model_version(model, version):
    model_path = f"models/model_v{version}.h5"
    model.save(model_path)
