
from tensorflow.keras import layers

def build_vae():
    encoder = tf.keras.Sequential([
        layers.InputLayer(input_shape=(28, 28, 1)),
        layers.Conv2D(32, 3, activation='relu', strides=2, padding='same'),
        layers.Conv2D(64, 3, activation='relu', strides=2, padding='same'),
        layers.Flatten(),
        layers.Dense(16, activation='relu')
    ])
    
    decoder = tf.keras.Sequential([
        layers.InputLayer(input_shape=(16,)),
        layers.Dense(7*7*64, activation='relu'),
        layers.Reshape((7, 7, 64)),
        layers.Conv2DTranspose(64, 3, activation='relu', strides=2, padding='same'),
        layers.Conv2DTranspose(32, 3, activation='relu', strides=2, padding='same'),
        layers.Conv2DTranspose(1, 3, activation='sigmoid', padding='same')
    ])
    return encoder, decoder
