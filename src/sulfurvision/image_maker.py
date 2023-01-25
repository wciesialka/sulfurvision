'''Module responsible for generating images.'''

# This file is part of sulfurvision.
# sulfurvision is free software: you can redistribute it and/or modify it under the 
# terms of the GNU General Public License as published by the Free Software Foundation, 
# version 3 of the License. sulfurvision is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
# details. You should have received a copy of the GNU General Public License along with
# sulfurvision. If not, see <https://www.gnu.org/licenses/>.

from importlib.resources import files
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

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
    base_ref = files("sulfurvision.data").joinpath('base.jpg')
    with base_ref.open('rb') as base_file:
        base = Image.open(base_file).convert("RGB")

    # Overlay the second image
    overlay = image.resize((IMAGEBOX[2], IMAGEBOX[3]), Image.BICUBIC).convert("RGBA")
    base.paste(overlay, box=(IMAGEBOX[0], IMAGEBOX[1]), mask=overlay)

    # Get the correct font size
    font_ref = files("sulfurvision.data").joinpath('impact.ttf')
    font_stream = font_ref.open('rb')

    max_font_size = 121 # max size
    min_font_size = 36 # min size
    font_size = max_font_size + 1
    size = None
    width = 0xFFFFFFFF
    height = 0

    font = None

    while (font_size > min_font_size) and (width > TEXTBOX[2]):
        font_size -= 1
        font = ImageFont.truetype(font_stream, font_size)
        size = font.getsize(text)
        width = size[0]
        height = size[1]
        font_stream.seek(0)

    def __wordwrap(_text: str):
        size = font.getsize(_text)
        width = size[0]
        # If the width of the text is less than the size of the textbox
        # then we can return a list with the text as the only element.
        if width <= TEXTBOX[2]:
            return [_text.strip()]
        # Find the right bound of where the string becomes too long
        temp = _text
        bound = len(temp)-1
        while width > TEXTBOX[2]:
            bound -= 1
            temp = temp[:bound]
            size = font.getsize(temp)
            width = size[0]
        # Try to find if there was a space before the right bound
        # that would be easier to split at.
        space = _text.rfind(" ", 0, bound)
        if space != -1:
            bound = space
        split = (_text[:bound], _text[bound:])
        return [split[0].strip(), *__wordwrap(split[1].strip())]

    wrapped_text = __wordwrap(text)

    def __draw_text(x: int, y: int, _text: str):
        draw = ImageDraw.Draw(base)
        border_size = max(1, font.size // 12)
        for i in range(1, border_size):
            # Draw the border first
            draw.text((x-i, y), _text, font=font, fill="black")
            draw.text((x+i, y), _text, font=font, fill="black")
            draw.text((x, y+i), _text, font=font, fill="black")
            draw.text((x, y-i), _text, font=font, fill="black")
            draw.text((x-i, y-i), _text, font=font, fill="black")
            draw.text((x+i, y-i), _text, font=font, fill="black")
            draw.text((x-i, y+i), _text, font=font, fill="black")
            draw.text((x+i, y+i), _text, font=font, fill="black")
            # Draw the text on top of the border
            draw.text((x, y), _text, font=font, fill="white")

    if len(wrapped_text) > 1:
        for i, segment in enumerate(wrapped_text):
            seg_size = font.getsize(segment)
            x = TEXTBOX[0] + (TEXTBOX[2] - seg_size[0]) / 2
            y = TEXTBOX[1]
            __draw_text(x, y + (height * i), segment)
    else:
        x = TEXTBOX[0] + (TEXTBOX[2] - width) / 2
        y = TEXTBOX[1] + (TEXTBOX[3] - height) / 2
        __draw_text(x, y, text)

    font_stream.close()

    return base
