from PIL import ImageFont

class MASKSVG:
    def __init__(self, width=1000, height=1000, text=None,padding=8, fontsize=100, font=r"C:\Windows\Fonts\arial.ttf"):
        self.font = font
        self.text = text
        self.fontsize = fontsize
        self.maxwidth = width
        self.maxheight = height
        self.data = ""
        self.padding = padding

        if type(self.padding) != int and self.padding < 0:
            raise ValueError("Padding must be a positive integer.")


    def func(self):
        try:
            font = ImageFont.truetype(font=self.font, size=self.fontsize)
        except OSError:
            raise FileNotFoundError(f"Font file '{self.font}' not found.")
        fontSize = font.getsize(self.text)
        return fontSize[0]  # Returning width

    def getBestFit(self):
        while self.func() >= self.maxwidth:
            self.fontsize -= 2
        print("Best fit: ", self.fontsize)
        return self.fontsize

    def generateSVG(self):
        self.fontsize = self.getBestFit()
        self.fontsize = self.fontsize - (self.fontsize // self.padding)

        fnt = ImageFont.truetype(self.font, size=self.fontsize)
        w, h = fnt.getsize(self.text)

        width = (self.maxwidth - w) // 2
        height = self.maxheight // 2

        svg = f"""<?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
            "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
            <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{self.maxwidth}" height="{self.maxheight}">
                <rect x="0" y="0" width="1000" height="1000" fill="coral" stroke="None" />
                <text font-size="{self.fontsize}" x="{width}" y="{height}" class="small">{self.text}</text>
            </svg>
            """

        self.data = svg
        return svg

    def save(self):
        with open("sample.svg", mode="w") as file:
            file.write(self.data)

zero = MASKSVG(
    font=f"C:\Windows\Fonts\BRLNSR.TTF",
    fontsize=200, 
    width=1000,
    height=1000,
    text="Aconite",
    padding=8
)

print(zero.generateSVG())

# zero.generateSVG()
# zero.save()
