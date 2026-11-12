from display_refactor.drivers import DisplayDriver

import base64

import pymupdf
from PIL import Image
from weasyprint import HTML, CSS

from jinja2 import Template

class Renderer():
    _display_driver: DisplayDriver | None
    _screen_dimensions: tuple[int,int]

    def __init__(self, display_driver: DisplayDriver):
        self._display_driver = display_driver
        self._screen_dimensions = self._display_driver.get_display_info()["dimensions"]

    def render_image(self, image: Image):
        self._display_driver.set_image(image)

    def render_view(self, view):
        pass

    def format_html_template(self, template: str, content):
        template = Template(template)
        return template.render(**content)

    def render_html_template(self, template) -> Image.Image:
        width, height = self._screen_dimensions

        page_css = f"""
            @page {{
                size: {width}px {height}px;
                margin: 0;
            }}

            html, body {{
                margin: 0;
                padding: 0;
                width: {width}px;
                height: {height}px;
            }}

            {css}
        """

        pdf_bytes = HTML(
            string=html,
            base_url=base_url,
        ).write_pdf(
            stylesheets=[CSS(string=page_css)]
        )

        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as pdf:
            if len(pdf) == 0:
                raise ValueError("WeasyPrint produced an empty PDF")

            page = pdf[0]

            pixmap = page.get_pixmap(
                matrix=pymupdf.Matrix(96 / 72, 96 / 72),
                colorspace=pymupdf.csRGB,
                alpha=False,
            )

            image = Image.frombytes(
                "RGB",
                (pixmap.width, pixmap.height),
                pixmap.samples,
            )

            if image.size != (width, height):
                image = image.resize(
                    (width, height),
                    Image.Resampling.LANCZOS,
                )
            image.save("current_view.png")
            return image