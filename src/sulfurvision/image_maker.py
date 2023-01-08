from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
import pkg_resources

# boxes use format x, y, dx, dy
TEXTBOX = (209, 9, 465, 111)
IMAGEBOX = (26, 344, 200, 200)

def make_image(image: Image.Image, text: str) -> Image.Image:
    '''Generate a sulfurvision image with an overlay and a text.

    :param image: Image to overlay.
    :type image: Image.Image
    :param text: Text to overlay.
    :type text: str
    :return: Generated image.
    :rtype: Image.Image
    '''

    # Get the base layer
    layer_0_stream = pkg_resources.resource_stream(__name__, 'data/base.jpg')
    base = Image.open(layer_0_stream).convert("RGB")

    # Overlay the second image
    overlay = image.resize((IMAGEBOX[2], IMAGEBOX[3]), Image.BICUBIC).convert("RGBA")
    base.paste(overlay, box = (IMAGEBOX[0], IMAGEBOX[1]), mask = overlay)

    # Get the correct font size
    font_stream = pkg_resources.resource_stream(__name__, 'data/impact.ttf')

    max_font_size = 121 # max size
    min_font_size = 36 # min size
    font_size = max_font_size + 1
    size = None
    w = 0xFFFFFFFF
    h = 0

    font = None

    while (font_size > min_font_size) and (w > TEXTBOX[2]):
        font_size -= 1
        font = ImageFont.truetype(font_stream, font_size)
        size = font.getsize(text)
        w = size[0]
        h = size[1]
        font_stream.seek(0)

    def wordwrap(_text: str):
        size = font.getsize(_text)
        w = size[0]
        if(w <= TEXTBOX[2]):
            return [_text.strip()]
        else:
            # find where the string becomes too long
            temp = _text
            i = len(temp)-1
            while(w > TEXTBOX[2]):
                i -= 1
                temp = temp[:i]
                size = font.getsize(temp)
                w = size[0]
            space = _text.rfind(" ", 0, i)
            if space != -1:
                i = space
            split = (_text[:i], _text[i:])
            return [split[0].strip(), *wordwrap(split[1].strip())]

    wrapped_text = wordwrap(text)

    def draw_text(x: int, y: int, _text: str):
        draw = ImageDraw.Draw(base)
        border_size = max(1, font.size // 12)
        for i in range(1, border_size):
            draw.text((x-i, y),   _text, font = font, fill="black")
            draw.text((x+i, y),   _text, font = font, fill="black")
            draw.text((x, y+i),   _text, font = font, fill="black")
            draw.text((x, y-i),   _text, font = font, fill="black")
            draw.text((x-i, y-i), _text, font = font, fill="black")
            draw.text((x+i, y-i), _text, font = font, fill="black")
            draw.text((x-i, y+i), _text, font = font, fill="black")
            draw.text((x+i, y+i), _text, font = font, fill="black")
            draw.text((x,   y),   _text, font = font, fill="white")

    if len(wrapped_text) > 1:
        for i, segment in enumerate(wrapped_text):
            seg_size = font.getsize(segment)
            x = TEXTBOX[0] + (TEXTBOX[2] - seg_size[0]) / 2
            y = TEXTBOX[1]
            draw_text(x, y + (h * i), segment)
    else:
        x = TEXTBOX[0] + (TEXTBOX[2] - w) / 2
        y = TEXTBOX[1] + (TEXTBOX[3] - h) / 2
        draw_text(x, y, text)

    return base