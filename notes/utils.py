# utils.py
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.shortcuts import render, redirect
from .forms import DocumentForm  

def resize_image(image, size=(1080, 1080)):  # Ideal Instagram size
    img = Image.open(image)

    # Convert to RGB if the image is in RGBA mode
    if img.mode == 'RGBA':
        img = img.convert('RGB')  # Convert RGBA to RGB


    img.thumbnail(size, Image.LANCZOS)

    # Save to a BytesIO object
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=85)
    img_file = ContentFile(img_io.getvalue(), name=image.name)
    return img_file
