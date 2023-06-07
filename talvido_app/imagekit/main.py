from .import imagekit
import base64


class ImagekitClient():
    def __init__(self, media):
        self.file = self.convert_to_binary(media)
        self.file_name = media.name

    def convert_to_binary(self, file):
        binary_file = base64.b64encode(file.read())
        return binary_file

    @property
    def upload_file(self):
        upload = imagekit.upload_file(
        file=self.file,
        file_name=self.file_name,
    )
        return upload.response_metadata.raw
