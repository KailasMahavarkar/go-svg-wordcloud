import os
import re

import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud


from svgPro.generateWords import *
from svgPro.makeMASK import Mask
from Improve.color.color import getRGB
from svgPro.wordfilter import searchWordFilterWrapper, searchWordFilter
from Improve.Improve import executorClosure, executor

context = {}

rootPath = os.path.dirname(os.path.abspath(__file__))
imagePath = os.path.join(rootPath, "cloud", "inPath")


class Basic:
    def __init__(
            self, query=None, margin=10, wordcount=70,
            scale=1, bgColor=None, stopType=stopBasic,
            repeat=True, pages=1, width=1000, height=1000,
            fontPath=None, rotation_ratio=1, colorMap=None, fontFamily=None,
            max_font_size=150, min_font_size=3,
            maskText=None, context=None, padding=8
    ):

        # padding max_text
        self.padding = padding

        # query
        self.query = query

        # search pages
        self.pages = pages

        # context
        self.context = context

        # get context
        if isinstance(context, list):
            self.context = {random.choice(self.context): random.randrange(3, 20) for _ in self.context}
        else:
            self.context = context()

        # width
        self.width = width

        # height
        self.height = height

        # rotation
        self.rotation_ratio = float(rotation_ratio)

        # fontPath
        self.fontPath = fontPath

        # scale factor
        self.scale = scale

        # repeat keywords
        self.repeat = repeat

        # replace specials from query
        self.querySave = re.sub('[^A-Za-z0-9]+', '', self.query).lower()

        # MAX wordcount
        self.wordcount = wordcount

        # max font size
        self.max_font_size = max_font_size

        # min font size
        self.min_font_size = min_font_size

        # margin
        self.margin = margin

        # making single ColorFunc
        self.colorFunc = None

        # masking text
        if maskText is None:
            self.maskText = self.query
        else:
            self.maskText = maskText

        if type(colorMap) == list:
            self.colorMap = ListedColormap(colorMap)
        elif type(colorMap) == str:
            if colorMap not in plt.colormaps():
                raise ValueError("ColorMap must be valid i.e {s}".format(s=plt.colormaps()))
            else:
                self.colorMap = colorMap
        else:
            raise ValueError("ColorMap must be type List ['#ac0000', '#ae0001']")

        myFonts = ["Acme", "Ubuntu", "Product Sans"]
        # font family
        if fontFamily is None:
            self.font = random.choice(myFonts)
        else:
            self.font = str(fontFamily)

        # font url
        self.font_url = "@import url(https://fonts.googleapis.com/css?family={});".format(self.font)

        # background color
        self.bgColor = bgColor

        # stop Type
        self.stopType = stopType

        self.font = r"C:\USERS\KAI\APPDATA\LOCAL\MICROSOFT\WINDOWS\FONTS\Product Sans Bold.ttf"

        self.mask, self.loc, self.maskFontSize = Mask(
            text=self.maskText,
            width=self.width,
            height=self.height,
            font=self.font,
            padding=self.padding
        ).makeMASK()

        # print(self.maskFontSize)

        self.mask = np.array(self.mask)

    def generateSVG(self):
        wc = WordCloud(max_words=self.wordcount,
                       normalize_plurals=True,
                       width=self.width,
                       height=self.height,
                       mask=self.mask,
                       margin=self.margin,
                       font_path=self.fontPath,
                       colormap=self.colorMap,
                       background_color=self.bgColor,
                       repeat=self.repeat,
                       scale=self.scale,
                       color_func=self.colorFunc,
                       max_font_size=self.max_font_size,
                       min_font_size=self.min_font_size,
                       prefer_horizontal=self.rotation_ratio,
                       random_state=1
                       ).generate_from_frequencies(self.context)
        return wc

    def saveJPG(self):
        self.generateSVG().to_file('temp.jpg')
        Image.open(fp='temp.jpg').show()

    def saveSVG(self):
        content = ''.join(self.generateSVG().to_svg())
        with open('abc.svg', mode='w+') as file:
            file.write(str(content))
        return content


if __name__ == "__main__":
    query = 'TOR'
    google = ["#4285f4", "#ea4335", "#fbbc05", "#34a853"]

    words = searchWordFilterWrapper(
        query=query,
        stoptypes=['max', 'corrected', 'negative'],
        singularize=False,
        minlength=3,
        minoccurence=2,
        mode=2
    )

    x = Basic(
        query=query,
        margin=0,
        repeat=True,
        maskText=query.capitalize(),
        min_font_size=5,
        max_font_size=50,
        rotation_ratio=1,
        padding=8,
        context=words,
        wordcount=300,
        pages=1,
        width=1920,
        height=1080,
        scale=2,
        colorMap=google,
        bgColor=getRGB('white'),
        fontFamily="Berlin Sans",
        # fontPath=r"C:\USERS\KAI\APPDATA\LOCAL\MICROSOFT\WINDOWS\FONTS\Product Sans Bold.ttf"
        fontPath=r"C:\Windows\Fonts\BRLNSDB.TTF"
    )
    x.generateSVG()
    x.saveJPG()
