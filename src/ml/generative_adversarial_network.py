
from tensorflow.keras import layers

def build_gan():
    generator = tf.keras.Sequential([
        layers.Dense(256, activation='relu', input_shape=(100,)),
        layers.Dense(512, activation='relu'),
        layers.Dense(1024, activation='relu'),
        layers.Dense(28*28, activation='tanh')
    ])
    
    discriminator = tf.keras.Sequential([
        layers.Dense(1024, activation='relu', input_shape=(28*28,)),
        layers.Dense(512, activation='relu'),
        layers.Dense(256, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    return generator, discriminator
