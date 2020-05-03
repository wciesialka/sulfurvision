from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os, io

PATH = os.path.abspath(os.path.dirname(__file__))
DATA = os.path.join(PATH,"data")

def lappend(l1,l2):
    for e in l2:
        l1.append(e)
    return l1

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
        self.lastspace = 0
        self.font = None

    def overlay_image(self):
        new_image = self.overlay.resize((TheMaker.IMAGEBOX[2],TheMaker.IMAGEBOX[3]),Image.BICUBIC)
        self.img.paste(new_image,box=(TheMaker.IMAGEBOX[0],TheMaker.IMAGEBOX[1]))

    def wordwrap(self,text):
        size = self.font.getsize(text)
        w = size[0]
        if(w <= TheMaker.TEXTBOX[2]):
            return [text.strip()]
        else:
            # find where the string becomes too long
            temp = text
            i = len(temp)-1
            while(w > TheMaker.TEXTBOX[2]):
                i -= 1
                temp = temp[:i]
                size = self.font.getsize(temp)
                w = size[0]
            space = text.rfind(" ",0,i)
            if space != -1:
                i = space
            split = (text[:i],text[i:])
            return lappend([split[0].strip()], self.wordwrap(split[1].strip()))

    def overlay_text(self):
        fpath = os.path.join(DATA,"impact.ttf")
        smax = 121 # max size
        smin = 36 # min size
        fsize = smax+1
        size = None
        w = 0xFFFFFFFF
        h = 0
        while (fsize > smin) and (w > TheMaker.TEXTBOX[2]):
            fsize -= 1
            self.font = ImageFont.truetype(fpath, fsize)
            size = self.font.getsize(self.text)
            w = size[0]
            h = size[1]
        wrapped_text = self.wordwrap(self.text)
        if len(wrapped_text) > 1:
            for i,segment in enumerate(wrapped_text):
                seg_size = self.font.getsize(segment)
                x = TheMaker.TEXTBOX[0] + (TheMaker.TEXTBOX[2]-seg_size[0])/2
                y = TheMaker.TEXTBOX[1]# + (TheMaker.TEXTBOX[3]-seg_size[1])/2
                self.draw_text(x,y + (h*i),segment)
        else:
            x = TheMaker.TEXTBOX[0] + (TheMaker.TEXTBOX[2]-w)/2
            y = TheMaker.TEXTBOX[1] + (TheMaker.TEXTBOX[3]-h)/2
            self.draw_text(x,y,self.text)

    def draw_text(self,x:int,y:int,text:str):
        draw = ImageDraw.Draw(self.img)
        border_size = max(1,self.font.size//12)
        for i in range(1,border_size):
            draw.text((x-i, y),   text, font=self.font, fill="black")
            draw.text((x+i, y),   text, font=self.font, fill="black")
            draw.text((x, y+i),   text, font=self.font, fill="black")
            draw.text((x, y-i),   text, font=self.font, fill="black")
            draw.text((x-i, y-i), text, font=self.font, fill="black")
            draw.text((x+i, y-i), text, font=self.font, fill="black")
            draw.text((x-i, y+i), text, font=self.font, fill="black")
            draw.text((x+i, y+i), text, font=self.font, fill="black")
            draw.text((x,   y),   text, font=self.font, fill="white")

    def show(self):
        self.img.show()

    def save(self,out):
        self.img.save(out)

    def as_bytes(self):
        b = None
        with io.BytesIO() as buf:
            self.img.save(buf,"JPEG")
            b = buf.getvalue()
        return b
