from Crypto.Hash import SHA256
import datetime
from PIL import Image
from io import BytesIO

def get_date_formatted(date):
    if date:
        return date.strftime("%d.%m.%Y")
    return ""

def hash_string(data):
    h = SHA256.new()
    h.update(str.encode(data, encoding="UTF-8"))
    c_hashed = h.hexdigest()
    return c_hashed

def hash_bytes(data):
    h = SHA256.new()
    h.update(data)
    c_hashed = h.hexdigest()
    return c_hashed

def validate_jpeg(image_bytes):
    try:
        image = Image.open(BytesIO(image_bytes))
        if image.format != "JPEG":
            return False
    except Exception:
        return False
    
    return True

def is_jpeg_magic(image_bytes):
    header = image_bytes[0:3]
    return header == b'\xff\xd8\xff'