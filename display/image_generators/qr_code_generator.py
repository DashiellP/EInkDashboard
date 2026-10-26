from config import config
from image_generators.image_generator import ImageGenerator
import qrcode

class QRCodeGenerator(ImageGenerator):
    _qrcode_target = config.SERVER_URL
    _qrcode_size = 21

    def generate(self):
        qr = qrcode.QRCode()
        qr.add_data(self._qrcode_target)
        qr.make(fit=True)
        image = qr.make_image(fill_color="black", back_color="white")
        image = image.convert("RGB")
        image = image.resize((480, 480))
        return image

