import traceback
import re

from config import config
from image_generators.image_generator import ImageGenerator
from font_fredoka_one import FredokaOne
from PIL import Image, ImageDraw, ImageFont

class ErrorPageGenerator(ImageGenerator):
    def generate(self, exception=None):
        if (exception is not None):
            exception_name = type(exception).__name__
            exception_description = str(exception)
            exception_traceback = traceback.format_exc()
        else:
            exception_name = "Unknown Error"
            exception_description = "An unknown error has occurred"
            exception_traceback = ""
        image = Image.new("P", self._dimensions, "#FFFFFF")
        draw = ImageDraw.Draw(image)
        font_path = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
        header_font = ImageFont.truetype(font_path, 36)
        name_font = ImageFont.truetype(font_path, 24)
        description_font = ImageFont.truetype(font_path, 16)
        traceback_font = ImageFont.truetype(font_path, 12)
        draw.text((20, 20), "ERROR", "#FF0000", header_font)
        draw.multiline_text((20, 72), self.wrap_text(exception_name, name_font, self._dimensions[0] - 40, draw), "#000000", name_font)
        draw.multiline_text((20, 112), self.wrap_text(exception_description, description_font, self._dimensions[0] - 40, draw), "#000000", description_font)
        draw.multiline_text((20, 152), self.wrap_text(exception_traceback, traceback_font, self._dimensions[0] - 40, draw), "#000000", traceback_font)
        return image