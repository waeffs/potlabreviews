import os
# pip install pillow
from PIL import Image

from datetime import datetime
from flask import url_for, current_app

def add_blog_pic(pic_upload):
    filename = pic_upload.filename

    storage_filename = filename

    filepath = os.path.join(current_app.root_path, 'static/blog_pics', storage_filename)

    # Play Around with this size.
    output_size = (340, 500)

    # Open the picture and save it
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename

def create_thumbnail(pic_upload):
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]

    storage_filename = filename + 'small.' + ext_type

    filepath = os.path.join(current_app.root_path, 'static/blog_pics/small', storage_filename)

    # Play Around with this size.
    output_size = (100, 80)

    # Open the picture and save it
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename
