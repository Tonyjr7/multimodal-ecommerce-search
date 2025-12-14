from PIL import Image
import io
import tensorflow as tf

def prepare_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((128, 128)) 
    img_array = tf.keras.utils.img_to_array(img)
    
    return tf.expand_dims(img_array, 0) 