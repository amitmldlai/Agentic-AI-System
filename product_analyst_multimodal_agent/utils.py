from PIL import Image
from io import BytesIO
from tempfile import NamedTemporaryFile
import requests

MAX_IMAGE_WIDTH = 300


def resize_image_for_display(image_file):
    """Resize image for display only, returns bytes."""

    # Check if the input is a URL or a file path
    if isinstance(image_file, str) and image_file.startswith('http'):
        # If it's a URL, download the image
        response = requests.get(image_file)
        img = Image.open(BytesIO(response.content))
    else:
        # If it's a file path or file-like object
        img = Image.open(image_file)
        image_file.seek(0) if hasattr(image_file, 'seek') else None

    # Resize the image based on aspect ratio
    aspect_ratio = img.height / img.width
    new_height = int(MAX_IMAGE_WIDTH * aspect_ratio)
    img = img.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)

    # Save the resized image to a buffer and return the byte data
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def save_uploaded_file(uploaded_file):
    """Save uploaded file or image from URL to a temporary file, returns file path."""

    if isinstance(uploaded_file, str) and uploaded_file.startswith('http'):
        # If the input is a URL, download the image
        response = requests.get(uploaded_file)
        img_data = response.content

        # Save the image data to a temporary file
        with NamedTemporaryFile(dir='.', suffix='.jpg', delete=False) as f:
            f.write(img_data)
            return f.name
    else:
        # If it's a file-like object (e.g., uploaded file)
        with NamedTemporaryFile(dir='.', suffix='.jpg', delete=False) as f:
            f.write(uploaded_file.getbuffer())
            return f.name