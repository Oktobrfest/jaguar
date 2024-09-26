import os
import io
import base64
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app
import string


class ImageProcessor:
    def __init__(self,
                 base_name=None,
                 save_directory=current_app.config["CROPPED_IMAGES_FOLDER"],
                 increment_mode="numeric",
                 custom_pattern=None,
                 s3_client=None,
                 s3_bucket=None):
        """
        Initializes the ImageProcessor with optional base_name for filenames and other settings.

        :param base_name: Base name to use for image filenames.
        :param save_directory: Directory to save images locally.
        :param increment_mode: Defines how filenames should increment (e.g., numeric, alphabetic).
        :param custom_pattern: Optional custom pattern for filename increments.
        :param s3_client: S3 client object.
        :param s3_bucket: S3 bucket name.
        """
        self.save_directory = save_directory
        self.s3_client = s3_client
        self.s3_bucket = s3_bucket
        self.base_name = base_name or "image"
        self.increment_mode = increment_mode
        self.custom_pattern = custom_pattern
        self.filename_counter = 0

    def generate_filename(self, extension="png", custom_suffix=None):
        """
        Generates a unique filename based on the base_name, increment_mode, optional suffix, and counter.

        :param extension: File extension (default is 'png').
        :param custom_suffix: Optional string to append to the filename.
        :return: Generated filename as a string.
        """
        self.filename_counter += 1

        # Choose increment pattern based on increment_mode
        if self.increment_mode == "numeric":
            increment = str(self.filename_counter)
        elif self.increment_mode == "alphabetic":
            increment = self._increment_alphabetic(self.filename_counter)
        elif self.increment_mode == "custom" and self.custom_pattern:
            increment = self.custom_pattern.format(self.filename_counter)
        else:
            raise ValueError(f"Invalid increment mode: {self.increment_mode}")

        # Build the filename
        filename = f"{self.base_name}_{increment}"

        # Append a custom suffix if provided
        if custom_suffix:
            filename += f"_{custom_suffix}"

        # Add the file extension
        filename = f"{filename}.{extension}"

        return filename

    def _increment_alphabetic(self, counter):
        """Converts a numeric counter to an alphabetic string (A, B, C, ..., Z, AA, AB, ...)."""
        alphabet = string.ascii_uppercase
        result = ""
        while counter > 0:
            counter, remainder = divmod(counter - 1, 26)
            result = alphabet[remainder] + result
        return result

    def save_image_locally(self, image, custom_suffix=None):
        """Save image to local directory and return the file path."""
        filename = self.generate_filename(custom_suffix=custom_suffix)
        save_path = os.path.join(self.save_directory, filename)

        with Image.open(image.stream) as image_data:
            image_data.save(save_path)

        return save_path

    def upload_image_to_s3(self, image, custom_suffix=None):
        """Upload image to S3 and return the URL."""
        if not self.s3_client or not self.s3_bucket:
            raise ValueError("S3 client or bucket not configured.")

        filename = self.generate_filename(custom_suffix=custom_suffix)
        file_stream = image.stream.read()

        # Upload the image to S3 with the generated filename
        self.s3_client.put_object(Bucket=self.s3_bucket, Key=filename,
                                  Body=file_stream, ContentType='image/png')

        image_url = f"https://{self.s3_bucket}.s3.amazonaws.com/{filename}"
        return image_url

    def encode_image_to_base64(self, image):
        """Encode image to base64 and return the encoded string."""
        with Image.open(image.stream) as image_data:
            img_byte_arr = io.BytesIO()
            image_data.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

        encoded_image = base64.b64encode(img_byte_arr).decode('utf-8')
        return f"data:image/png;base64,{encoded_image}"

    def process_image(self, image, upload_to_s3=False, encode=False,
                      custom_suffix=None):
        """
        Process the image by saving it locally or uploading to S3, optionally encoding it.
        Returns the image URL or base64 encoded string based on parameters.

        :param image: The image to process.
        :param upload_to_s3: If True, the image will be uploaded to S3.
        :param encode: If True, the image will be encoded to base64.
        :param custom_suffix: Optional suffix to append to the filename.
        :return: URL or encoded string of the processed image.
        """
        if upload_to_s3:
            return self.upload_image_to_s3(image, custom_suffix=custom_suffix)
        elif encode:
            return self.encode_image_to_base64(image)
        else:
            return self.save_image_locally(image, custom_suffix=custom_suffix)
