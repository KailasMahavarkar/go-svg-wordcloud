import random
from PIL import Image
from shapely.geometry import Polygon

from Save.color import getRGB


# sys.setrecursionlimit(100000)


def checkExisting(rect1, main):
    result = all([overlap(rect1=rect1, rect2=rect2) for rect2 in main])
    return result


def overlap(rect1, rect2):
    p1 = Polygon([rect1[0], rect1[1], rect1[2], rect1[3]])
    p2 = Polygon([rect2[0], rect2[1], rect2[2], rect2[3]])
    return p1.intersects(p2)


def makeRect(width, height, color):
    return Image.new(mode='RGB', size=(width, height), color=color)


class ClothSave:
    def __init__(self):
        self.font = r"C:\Windows\Fonts\BRLNSDB.TTF"
        self.pos = {}

        self.poly_w, self.poly_h = 100, 100
        self.bg_w, self.bg_h = 1000, 1000
        self.mask_w, self.mask_h = 500, 500

        self.ivory = getRGB('ivory')
        self.black = getRGB('black')
        self.red = getRGB('red')
        self.ran_counter = 0

        self.bg = makeRect(width=self.bg_w, height=self.bg_h, color=self.ivory)
        self.poly = makeRect(width=self.poly_w, height=self.poly_h, color=self.red)
        self.mask = makeRect(width=self.mask_w, height=self.mask_h, color=self.black)

    def drawMask(self):
        self.bg.paste(im=self.mask, box=(self.mask_w // 2, self.mask_h // 2))

    def drawPoly(self):
        loaded_bg = self.bg.load()

        self.ran_counter += 1
        random_X = random.randrange(0, self.bg_w - self.poly_w)
        random_Y = random.randrange(0, self.bg_h - self.poly_h)

        p1 = random_X, random_Y
        p2 = random_X + self.poly_h, random_Y
        p3 = random_X + self.poly_w, random_Y + self.poly_h
        p4 = random_X, random_Y + self.poly_h

        x0y0 = loaded_bg[p1]
        x1y0 = loaded_bg[p2]
        x1y1 = loaded_bg[p3]
        x0y1 = loaded_bg[p4]

        if all([i == self.black for i in [x0y0, x1y0, x1y1, x0y1]]):
            print(x0y0, x1y0, x1y1, x0y1)
            self.bg.show()
            print('ran', self.ran_counter)
            self.bg.paste(im=self.poly, box=(random_X, random_Y))
            self.pos.update({(p1, p2, p3, p4): None})
        else:
            self.drawPoly()

    def showBG(self):
        self.bg.show()

    def pos(self):
        return self.pos


x = ClothSave()
x.drawMask()

for _ in range(20):
    x.drawPoly()

print(x.pos.keys())
print(len(x.pos))

x.showBG()
