from PIL import Image, ImageDraw, ImageFont


def generateSVG(width=1000, height=1000, text=None, fontsize=100, font=r"C:\Windows\Fonts\BRLNSDB.TTF"):
    fnt = ImageFont.truetype(size=100, font=r"C:\Windows\Fonts\BRLNSDB.TTF")
    w, h = fnt.getsize(text=text)

    print(w, h)

    svg = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">""" + \
          """<svg xmlns="http://www.w3.org/2000/svg" version="1.1"
        width="{width}" height="{height}">""".format(width=width, height=height) + \
          """
          
        <rect x="0" y="0" width="1000" height="1000" fill="coral"
        stroke="None" />
        <text font-size="{fontsize}" x="{x}" y="{y}" class="small">{text}</text>
        <div style="text-align:center;">
        <p>HELLO </p>
        </div>
        </svg>   
    """.format(fontsize=fontsize, x=((width - w) // 2), y=(height - h) // 2, text=text)
    print((width - w) // 2)
    print((height - h) // 2)
    return svg


data = generateSVG(fontsize=50, width=1000, height=1000, text="watermelon")

file = open("sample.svg", mode="w")
file.write(data)
file.close()
