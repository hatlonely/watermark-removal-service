import pytest
from PIL import Image
import base64
from uri_encoder import encode_image_to_uri, decode_uri_to_image

def test_encode_image_to_uri():
    image_base64 = ""
    with open("../test/1.png", "rb") as f:
        bytes = f.read()
        image_base64 = base64.b64encode(bytes).decode()
    
    image = Image.open("../test/1.png")
    assert encode_image_to_uri(image, "png") == f"data:image/png;base64,{image_base64}"

def test_decode_uri_to_image():
    image = Image.open("../test/1.png")
    image_uri = encode_image_to_uri(image, "png")
    assert decode_uri_to_image(image_uri).tobytes() == image.tobytes()
