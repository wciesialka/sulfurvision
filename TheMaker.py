from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os

PATH = os.path.abspath(os.path.dirname(__file__))
DATA = os.path.join(PATH,"data")

class TheMaker:

    # boxes use format x, y, dx, dy
    TEXTBOX = (209,9,465,111)
    IMAGEBOX = (26, 344, 200, 200)
    BASE_PATH = os.path.join(DATA,"base.jpg")
    
    def __init__(self,img:Image.Image,text:str):
        if not isinstance(img,Image.Image):
            raise TypeError(f"img should be type Image, not {type(img)}")
        if not isinstance(text,str):
            raise TypeError(f"text should be type str, not {type(text)}")
        self.text = text
        self.overlay = img
        self.img = Image.open(TheMaker.BASE_PATH)

    def overlay_image(self):
        new_image = self.overlay.resize((TheMaker.IMAGEBOX[2],TheMaker.IMAGEBOX[3]),Image.BICUBIC)
        self.img.paste(new_image,box=(TheMaker.IMAGEBOX[0],TheMaker.IMAGEBOX[1]))

    def overlay_text(self):
        fpath = os.path.join(DATA,"impact.ttf")
        smax = 144 # max size
        smin = 36 # min size
        fsize = smax+1
        size = None
        w = 0xFFFFFFFF
        h = 0
        while (fsize > smin) and (w > TheMaker.TEXTBOX[2]):
            fsize -= 1
            font = ImageFont.truetype(fpath, fsize)
            size = font.getsize(self.text)
            w = size[0]
            h = size[1]
        x = TheMaker.TEXTBOX[0] + (TheMaker.TEXTBOX[2]-w)/2
        y = TheMaker.TEXTBOX[1] + (TheMaker.TEXTBOX[3]-h)/2
        self.draw_text(x,y,font)

    def draw_text(self,x:int,y:int,font:ImageFont.truetype):
        draw = ImageDraw.Draw(self.img)
        border_size = max(1,font.size//12)
        for i in range(1,border_size):
            draw.text((x-i, y), self.text, font=font, fill="black")
            draw.text((x+i, y), self.text, font=font, fill="black")
            draw.text((x, y+i), self.text, font=font, fill="black")
            draw.text((x, y-i), self.text, font=font, fill="black")
            draw.text((x-i, y-i), self.text, font=font, fill="black")
            draw.text((x+i, y-i), self.text, font=font, fill="black")
            draw.text((x-i, y+i), self.text, font=font, fill="black")
            draw.text((x+i, y+i), self.text, font=font, fill="black")
            draw.text((x,   y),   self.text, font=font, fill="white")

    def show(self):
        self.img.show()

    def save(self,out):
        self.img.save(out)