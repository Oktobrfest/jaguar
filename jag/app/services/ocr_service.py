import os
from PIL import Image
import pytesseract


def perform_ocr(image_folder: str = '/app/static/images') -> str:
    """local OCR via pytesseract"""
    files = [os.path.join(image_folder, f)
             for f in os.listdir(image_folder)
             if f.endswith('.png')]
    if not files:
        raise FileNotFoundError("No images found")

    latest_image_path = sorted(files)[-1]

    try:
        img = Image.open(latest_image_path)
        text = pytesseract.image_to_string(img)
        return text
    except FileNotFoundError:
        raise FileNotFoundError("Image not found")
    except Exception as e:
        raise Exception(f"Error performing OCR: {str(e)}")
