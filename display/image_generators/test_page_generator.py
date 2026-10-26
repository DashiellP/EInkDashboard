from config import config
from image_generators.image_generator import ImageGenerator

class TestPageGenerator(ImageGenerator):
    _endpoint = config.SERVER_URL + "node/color-test?key=" + config.SECRET_KEY

    def generate(self):
        return super().get_image_from_uri(self._endpoint)