import os
import secrets
from PIL import Image
from flask import current_app

def save_profile_image(form_image):
    """Save users profile image in the file system"""

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/profile_images', image_fn)

    output_size = (125, 125)
    resized_image = Image.open(form_image)
    resized_image.thumbnail(output_size)

    resized_image.save(image_path)

    return image_fn