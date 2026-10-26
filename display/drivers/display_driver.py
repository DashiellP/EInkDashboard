import inky.auto
from PIL import Image, ImageDraw, ImageFont

from utils.state_manager import StateManager

class DisplayDriver():
    _display = None
    state_manager : StateManager


    def __init__(self):
        self.state_manager = StateManager()
        self.state_manager.set_state_to_working()
        self._display = inky.auto(ask_user=True, verbose=True)
        self._display.speed = self._display.MEDIUM
        self.state_manager.set_state_to_idle()
    
    def set_image(self, image, saturation=0.5):
        
        self.state_manager.set_state_to_working()
        image = self._resize_image(image, self._display.width, self._display.height)
        # image = imageprocessing.process_colors_for_display(image);
        self._display.set_image(image, saturation = 0.5)
        self._display.show(image)
        self.state_manager.set_state_to_idle()

    def get_display_info(self):
        return {
            "dimensions": (self._display.width, self._display.height)
        }

    def _resize_image(self, image, max_width, max_height):
        target_width = -1
        target_height = -1
        new_image = Image.new('RGB', (max_width, max_height))
        if image.width > (max_width / max_height) * image.height:
            target_width = max_width
            target_height = round(image.height * (max_width / image.width))
        else:
            target_height = max_height
            target_width = round(image.width * (max_height / image.height))
        image = image.resize((target_width, target_height))
        x = (int)((max_width - target_width) / 2)
        y = (int)((max_height - target_height) / 2)
        new_image.paste(image, (x,y))
        return new_image
