
from tensorflow.keras.applications import VGG16

def load_pretrained_model():
    model = VGG16(weights='imagenet', include_top=False)
    return model
