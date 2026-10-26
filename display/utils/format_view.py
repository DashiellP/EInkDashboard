import base64
import requests
from html2pic import Html2Pic

def format_view(view_file_path, values):
    with open(view_file_path, "r", encoding="utf-8") as file:
        content = file.read()
        return content.format(**values)

def fetch_image_data(image_url):
    response = requests.get(image_url, timeout=15)
    response.raise_for_status()
    encoded = base64.b64encode(response.content).decode("ascii")
    return "data:image/png;base64," + encoded

import pymupdf
from PIL import Image
from weasyprint import HTML, CSS


def html_to_image(
    html: str,
    dimensions,
    css: str = "",
    base_url: str | None = None,
) -> Image.Image:
    """
    Render HTML/CSS to a Pillow RGB image.
    """

    width, height = dimensions

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

        # Construct the Pillow image directly from raw pixel data.
        image = Image.frombytes(
            "RGB",
            (pixmap.width, pixmap.height),
            pixmap.samples,
        )

        # Ensure exact output dimensions.
        if image.size != (width, height):
            image = image.resize(
                (width, height),
                Image.Resampling.LANCZOS,
            )
        image.save("test2.png")
        return image