import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.append(r"C:\Zero\Improve\color")
rootPath = os.path.dirname(os.path.abspath(__file__))
imagePath = os.path.join(rootPath, "cloud", "inPath")

class MaskText:
    def __init__(self, width=1000, height=500, font=r"C:\Windows\Fonts\BRLNSDB.TTF", fontSize=None, padding=8, text=None):
        self.width = width
        self.height = height
        self.font = font
        self.text = text
        self.fontSize = fontSize
        self.padding = padding
        self.auto_padding = True
        self.text_width = 0
        self.text_height = 0
        self.shape = (0, 0)

        if self.fontSize is None:
            self.fontSize = 1000

    def getBestFit(self):
        min_size = 0
        max_size = self.fontSize
        while min_size <= max_size:
            mid_size = (min_size + max_size) // 2
            font = ImageFont.truetype(font=self.font, size=mid_size)
            self.text_width, self.text_height = font.getsize(self.text)
            if self.text_width + 2 * self.padding <= self.width:
                min_size = mid_size + 1
                self.fontSize = mid_size
            else:
                max_size = mid_size - 1
    
    def autoAdjustPadding(self):
        if self.width - self.text_width < 0:
            self.padding = self.padding + abs(self.width - self.text_width) // 2
        if self.height - self.text_height < 0:
            self.padding = self.padding + abs(self.height - self.text_height) // 2
            

    def makeMASK(self):
        self.getBestFit()
        self.autoAdjustPadding()

        if type(self.padding) == int and self.padding > 0:
            self.fontSize = self.fontSize - (self.fontSize // self.padding)

        out = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        fnt = ImageFont.truetype(self.font, size=self.fontSize)
        w, h = fnt.getsize(text=self.text)

        d = ImageDraw.Draw(out)
        shape = ((self.width - w) // 2, (self.height - h) // 2)
        d.text(
            shape,
            text=self.text,
            font=fnt,
            fill=(0, 0, 0)
        )
        return out, shape, self.fontSize

    def makeSVG(self, shouldWrite=False, svgName="sample.svg"):
        self.getBestFit()
        svg = f"""<?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
            "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
            <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{self.width}" height="{self.height}">
                <rect x="0" y="0" width="1000" height="1000" fill="coral" stroke="None" />
                <text font-size="{self.fontSize}" x="{self.text_width}" y="{self.text_height}" class="small">{self.text}</text>
            </svg>
            """
        if shouldWrite:
            with open(svgName, mode="w") as file:
                file.write(svg)

        return svg
 
if __name__ == '__main__':
    query = 'Aconite'
    y = MaskText(
        width=1000,
        height=1000,
        padding=8,
        text=query,
        font = r"C:\Windows\Fonts\BRLNSDB.TTF"
    )
    
    x = y.makeMASK(shouldWrite=True)
    print("x -->", x)


    # y[0].show()


# i have checked the font location and PIL is installed correctly.. 
# find the bug in code... there are no errors from my side