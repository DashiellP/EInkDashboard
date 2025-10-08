from drivers import DisplayDriver
from image_generators.random_screenshot_generator import RandomScreenshotGenerator
from utils.state_manager import StateManager

import numpy
from PIL import Image

class DisplayService():
    _display_driver : DisplayDriver

    state_manager : StateManager

    def __init__(self, display_driver):
        self._display_driver = display_driver
        self.state_manager = StateManager()
        self.state_manager.add_child(self._display_driver.state_manager)

    def update_image(self, image):
        self._display_driver.set_image(image)

    DESATURATED_PALETTE = [
        [0, 0, 0],
        [255, 255, 255],
        [255, 255, 0],
        [255, 0, 0],
        [0, 0, 255],
        [0, 255, 0],
        [0, 200, 255],
        [255, 0, 136]]

    SATURATED_PALETTE = [
        [0, 0, 0],
        [161, 164, 165],
        [208, 190, 71],
        [156, 72, 75],
        [61, 59, 94],
        [58, 91, 70],
        [61, 99, 110],
        [120, 65, 86]]

    def _palette_blend(self, saturation, dtype="uint8"):
        saturation = float(saturation)
        palette = []
        for i in range(len(self.SATURATED_PALETTE)):
            rs, gs, bs = [c * saturation for c in self.SATURATED_PALETTE[i]]
            rd, gd, bd = [c * (1.0 - saturation) for c in self.DESATURATED_PALETTE[i]]
            if dtype == "uint8":
                palette += [int(rs + rd), int(gs + gd), int(bs + bd)]
            if dtype == "uint24":
                palette += [(int(rs + rd) << 16) | (int(gs + gd) << 8) | int(bs + bd)]
        return palette

    def _convert_image(self, image):
        dither = Image.Dither.FLOYDSTEINBERG

        # Image size doesn't matter since it's just the palette we're using
        palette_image = Image.new("P", (1, 1))

        if image.mode == "P":
            # Create a pure colour palette from DESATURATED_PALETTE
            palette = numpy.array(DESATURATED_PALETTE, dtype=numpy.uint8).flatten().tobytes()
            palette_image.putpalette(palette)

            # Assume that palette mode images with an unset palette use the
            # default colour order and "DESATURATED_PALETTE" pure colours
            if not image.palette.colors:
                image.putpalette(palette)

            # Assume that palette mode images with exactly six colours use
            # all the correct colours, but not exactly in the right order.
            if len(image.palette.colors) == len(self.SATURATED_PALETTE):
                dither = Image.Dither.NONE
        else:
            # All other image should be quantized and dithered
            palette = self._palette_blend(0.5)
            palette_image.putpalette(palette)

        dither = Image.Dither.NONE
        image = image.convert("RGB").quantize(len(self.SATURATED_PALETTE), palette=palette_image, dither=dither)
        return image