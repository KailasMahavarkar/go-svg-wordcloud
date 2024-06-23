import random
import svgwrite
import os
import pathlib
import json
from svgwrite.extensions import Inkscape
from wordcloud import STOPWORDS

from generateWords import generateWords

dwg = svgwrite.Drawing('../customCloud/test.svg', profile='full', size=(640, 480))
inkscape = Inkscape(dwg)

top_layer = inkscape.layer(label="Top LAYER 1", locked=True)

dwg.add(top_layer)

line = dwg.line((100, 100), (300, 100), stroke=svgwrite.rgb(10, 10, 16, '%'), stroke_width=10)
top_layer.add(line)

text = dwg.text('Google', insert=(100, 100),font_family="Product Sans", font_size=100, fill='red')
top_layer.add(text)

nested_layer = inkscape.layer(label="Nested LAYER 2", locked=False)
top_layer.add(nested_layer)

text = dwg.text('Test2', insert=(100, 200), font_size=100, fill='blue')
nested_layer.add(text)

dwg.save()

class generateCloud:
    def __init__(self, width=500, height=500, query="games"):
        self.width = width
        self.height = height
        self.query = query
        self.fileName = "cloud/data/{}.svg".format(self.query)
        self.dirName = pathlib

        if pathlib.Path("cloud/json/{}.json".format(query)).is_file():
            ftr = open("cloud/json/{}.json".format(self.query), 'r', encoding="UTF-8")
            self.context = ftr.read()
            ftr.close()
        else:
            self.context = json.dumps(generateWords(query, stopType=["IOS"]))
            ftw = open("cloud/json/{}.json".format(self.query), 'w', encoding="UTF-8")
            ftw.write(self.context)
            ftw.close()

        try:
            os.mkdir("cloud")
            os.mkdir("cloud/data")
            os.mkdir("cloud/json")
        except FileExistsError:
            print("directory exists")

        try:
            os.remove(self.fileName)
        except FileNotFoundError:
            print("Error Handled")
        self.svgDoc = svgwrite.Drawing(filename=self.fileName,
                                       size=(width, height))

    def drawRectangle(self):
        self.svgDoc.add(
            self.svgDoc.rect(
                insert=(0, 0),
                size=(self.width, self.height),
                stroke_width=random.randrange(0, 50),
                stroke="red",
                fill="pink",
            ))

    def drawText(self):
        self.svgDoc.add(self.svgDoc.text("Hello World",
                                         insert=(100, 50)))

    def printDocument(self):
        # print(self.svgDoc.tostring())
        print(self.fileName)

    def saveDocument(self):
        self.svgDoc.save()


x = generateCloud(1000, 1000, query="mutation")
x.printDocument()
x.drawRectangle()
x.drawText()
x.saveDocument()

#
# svg_document.add(svg_document.rect(insert=(0, 0),
#                                    size=("200px", "100px"),
#                                    stroke_width="1",
#                                    stroke="black",
#                                    fill="rgb(255,255,0)"))
#
#
#
# print(svg_document.tostring())
#
# svg_document.save()
