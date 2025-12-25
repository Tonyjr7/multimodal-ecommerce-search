from PIL import Image
import io
import tensorflow as tf

def prepare_image(image_bytes: bytes) -> tf.Tensor:
    """
    Prepares an image for processing by resizing it to 128x128 and converting it to a tensor.

    Args:
        image_bytes (bytes): The image file bytes.

    Returns:
        tf.Tensor: The prepared image tensor.
    """
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((128, 128)) 
    img_array = tf.keras.utils.img_to_array(img)
    
    return tf.expand_dims(img_array, 0) 