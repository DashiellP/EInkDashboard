from image_generators import ImageGenerator

class View():
    _image_generator : ImageGenerator
    _update_period : int

    _base_priority = 0

    def get_priority(self):
        return self._base_priority

    def get_image(self):
        return self._image_generator.generate()