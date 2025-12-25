import pickle
import tensorflow as tf
import logging

import settings

# Configure logging
logger = logging.getLogger(__name__)

"""Load class names"""
try:
    with open(settings.CLASS_NAMES_PATH, 'rb') as f:
        class_names = pickle.load(f)
except Exception as e:
    logger.error(f"Error loading class names: {e}")
    class_names = []

"""GOLDILOCKS ARCHITECTURE"""
# FIX: Define architecture explicitly to bypass 'InputLayer' config error
def build_goldilocks_model(num_classes):
    """
    Builds a Goldilocks architecture for image classification.

    Args:
        num_classes (int): The number of classes in the dataset.

    Returns:
        tf.keras.Model: The compiled model.
    """
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(128, 128, 3)),
        tf.keras.layers.Rescaling(1./255),
        
        # Included these to match the saved weight shapes exactly
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.1),
        tf.keras.layers.RandomZoom(0.1),
        
        # Convolutional layers
        tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        
        tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        
        tf.keras.layers.Conv2D(128, 3, padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        
        # Fully connected layers
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    return model

try:
    cnn_model = build_goldilocks_model(len(class_names))
    cnn_model.load_weights(settings.CNN_MODEL_PATH)
    logger.info("CNN model loaded successfully")
except Exception as e:
    logger.error(f"Error loading CNN model: {e}")
    cnn_model = None