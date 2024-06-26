import base64
import io
from PIL import Image

# format: image/png, image/jpeg, image/gif
def encode_image_to_uri(image: Image, format: str) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    return f"data:image/{format};base64,{base64.b64encode(buffered.getvalue()).decode()}"


def decode_uri_to_image(uri: str) -> Image:
    data_format, encode_bytes = uri.split(";")
    format = data_format.split("/")[1]
    bytes = encode_bytes.split(",")[1]
    return Image.open(io.BytesIO(base64.b64decode(bytes)), formats=[format])
