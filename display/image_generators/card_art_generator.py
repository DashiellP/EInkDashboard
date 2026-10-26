from config import config
from image_generators.image_generator import ImageGenerator

class CardArtGenerator(ImageGenerator):
    _screenshot_endpoint = config.SERVER_URL + "randomcardart.php?key=" + config.SECRET_KEY

    def generate(self):
        return super().get_image_from_uri(self._screenshot_endpoint)