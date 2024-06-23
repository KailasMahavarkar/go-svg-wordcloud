import random
from string import hexdigits
from contextlib import suppress
from typing import Union, List, Tuple, NewType
from colorbase import colorBase


ColorType = Union[Tuple[int, int, int], List[int, int, int], str]



class COLOR:
    def __init__(self, color: ColorType):
        self.colorBase = colorBase
        self.color = color
        self.rand = lambda minimum=0, maximum=255: random.randint(
            minimum, maximum)
        self.value = (0, 0, 0)

        if isinstance(color) == str:
            # color should be 6 alphabets after removing '#' if it exists
            if len(color) == 6:
                self.value = self.hex_to_rgb(color)
            else:
                raise ValueError('Hex color should be 6 characters long')

        raise TypeError('Color must be a list or tuple')

    # ---------------------------- HELPERS ------------------------------
    @staticmethod
    def saturate(value):
        return max(0.0, min(1.0, value))

    # ---------------------------- FETCHERS ------------------------------

    def getRandomName(self):
        return random.choice(self.colorBase)[0]

    def getRandomColor(self):
        randomColor = self.getRandomName()
        return {randomColor: self.colorBase[randomColor]}

    def getRandomRGB(self):
        return self.rand(), self.rand(), self.rand()

    def getRandomRGBA(self):
        return self.rand(), self.rand(), self.rand(),  round(random.uniform(0, 1), 2)

    def getRandomHex(self):
        return tuple(self.colorBase[self.getRandomName()]['hex'])

    def getColor(self, color: str) -> dict:
        try:
            return {color: self.colorBase[color]}
        except KeyError:
            return {'black': self.colorBase['black']}

    def getRGB(self, color):
        """
            :type color: object
        """
        if color in self.colorBase.keys():
            return tuple(self.colorBase[color]['rgb'])
        else:
            return tuple(self.colorBase['black']['rgb'])

    # ---------------------------- VALIDATORS ------------------------------

    @staticmethod
    def isRGB(color: tuple):
        if len(color) == 3:
            return all([x <= 255 for x in color])
        raise False

    @staticmethod
    def isHex(color):
        with suppress(Exception):
            color = color.lstrip('#')

            # padding '0' color
            while len(color) < 6:
                color = color + '0'

            if type(color) == str and len(color) == 6:
                return all([h.upper() in hexdigits for h in color])

        return False

    # ---------------------------- CONVERTERS ------------------------------

    def hex_to_rgb(self):
        return tuple(int(self.color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self):
        if type(self.color) == list or type(self.color) == tuple:
            return "#{:02x}{:02x}{:02x}".format(self.color[0], self.color[1], self.color[2])

        # throw exception

    def hue_to_rgb(self, hue):
        r = abs(hue * 6.0 - 3.0) - 1.0
        g = 2.0 - abs(hue * 6.0 - 2.0)
        b = 2.0 - abs(hue * 6.0 - 4.0)
        return self.saturate(r), self.saturate(g), self.saturate(b)

    def hsl_to_rgb(self, hsl: Union[tuple, list]):
        h = hsl[0]
        s = hsl[1]
        l = hsl[2]

        r, g, b = self.hueRGB((h, s, l))
        c = (1.0 - abs(2.0 * l - 1.0)) * s
        r = (r - 0.5) * c + l
        g = (g - 0.5) * c + l
        b = (b - 0.5) * c + l
        return r, g, b

    # ---------------------------- FEATURES ------------------------------

    def indec_color(self, color: Union[str, tuple, list], difference: int = 1):
        """
            increments or decrements value by specified difference

            :param color: hex string or rgb tuple or rgb list
            :param difference: increment or decrement by 'n'
            :return: incremented hex string | rgb tuple
        """
        conversion_flag = False
        if isinstance(color, str) and self.isHex(color=color):
            color = self.hexRGB(color)
            conversion_flag = True

        # Handling -> Invalid length
        if len(color) != 3:
            return False

        # Handling -> Invalid type
        if not all([isinstance(x, int) for x in color]):
            return False

        if self.isRGB(color=color):
            a = color[0]
            b = color[1]
            c = color[2]

            c += difference

            if c == 256:
                c = 0
                b += difference

                if b == 256:
                    b = 0
                    if 0 < a < 255:
                        a += difference
                    else:
                        a, b, c = 255, 255, 255

            if conversion_flag:
                return self.rgbHEX((a, b, c))
            else:
                return a, b, c


if __name__ == '__main__':
    c = COLOR(color='#ac0000')
    print(c.hex_to_rgb())
    # print(c.getColor('peachpuff'))