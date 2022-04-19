import os
import secrets
from PIL import Image
from flask import current_app

def save_post_image(form_image):
    """Save post header image in the file system"""

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/post_images', image_fn)

    output_size = (1920, 1080)
    resized_image = Image.open(form_image)
    resized_image.thumbnail(output_size)

    resized_image.save(image_path)

    return image_fn