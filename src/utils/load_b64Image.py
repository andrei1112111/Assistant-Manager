import io
import base64
from PIL import Image


def load_b64Image(im_b64):
    # convert it into bytes
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))

    return img
