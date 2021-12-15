import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.append(r"C:\Zero\Improve\color")
rootPath = os.path.dirname(os.path.abspath(__file__))
imagePath = os.path.join(rootPath, "cloud", "inPath")


class Mask:
    def __init__(self, width=1000, height=500, font=r"C:\Windows\Fonts\BRLNSDB.TTF", fontSize=None,padding=8, text=None):
        self.width = width
        self.height = height
        self.font = font
        self.text = text
        self.fontSize = fontSize
        self.padding = padding

        if self.fontSize is None:
            self.fontSize = 1000

    def func(self):
        font = ImageFont.truetype(font=self.font, size=self.fontSize)
        fontSize = font.getsize(text=self.text)
        return fontSize[0]

    def getBestFit(self):
        while self.func() >= self.width:
            self.fontSize -= 2
            self.func()
        return self.fontSize

    def makeMASK(self):
        fontSize = self.getBestFit()
        if type(self.padding) == int and self.padding > 0:
            fontSize = fontSize - (fontSize // self.padding)

        out = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        fnt = ImageFont.truetype(self.font, size=fontSize)
        w, h = fnt.getsize(text=self.text)

        d = ImageDraw.Draw(out)
        d.text(
            ((self.width - w) // 2, (self.height - h) // 2),
            text=self.text,
            font=fnt,
            fill=(0, 0, 0)
        )

        return out, ((self.width - w) // 2, (self.height - h) // 2), fontSize


if __name__ == '__main__':
    query = 'Resume Filterer'
    y = Mask(
        text=query,
        width=2000,
        height=1000,
        fontSize=1000,
        padding=5,
        font=r"C:\Windows\Fonts\BRLNSDB.TTF"
    ).makeMASK()

    y[0].show()