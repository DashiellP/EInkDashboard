import requests
import re
from io import BytesIO
import PIL
import textwrap

class ImageGenerator():
    _dimensions = None

    def __init__(self, dimensions=None):
        self._dimensions = dimensions

    def generate(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_image_from_uri(self, image_uri):
        image = None
        try:
            if (image_uri.split("://")[0] in ["http", "https"]):
                response = requests.get(image_uri)
                image = PIL.Image.open(BytesIO(response.content))
            else:
                image = PIL.Image.open(image_uri)
        except FileNotFoundError:
            raise FileNotFoundError("Failed to load image at '{0}'.".format(image_uri))
        except PIL.UnidentifiedImageError:
            raise PIL.UnidentifiedImageError("Failed to load image at '{0}'.".format(image_uri))
        return image

    def wrap_text(self, text, font, max_width, draw):
        lines = []
        preexisting_lines = text.split("\n")
        for line in preexisting_lines:
            words = re.split("/\b/", line)
            current_line = ''
            for word in words:
                if word == " ":
                    continue
                test_line = current_line + ' ' + word if current_line else word
                width = draw.textlength(test_line, font=font)
                if width <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line.rstrip())
                    current_line = word
            if current_line:
                lines.append(current_line.rstrip())
        return "\n".join(lines)
