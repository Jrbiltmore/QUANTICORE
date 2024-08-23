
import tensorflow as tf

def build_meta_model():
    base_model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False)
    meta_model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(10)
    ])
    return meta_model
