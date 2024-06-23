import random as rd
import json
from colorbase import colorBase

random_color_choice = rd.choice(list(colorBase.keys()))
random_color = {random_color_choice: colorBase[random_color_choice]}


# helpers
def clamp(value: int, min_value: int, max_value: int):
    return max(min_value, min(max_value, value))


def saturate(value: int):
    return clamp(value, 0.0, 1.0)


# fetchers
def getRandomName():
    return random_color_choice


def getRandomRGB():
    return random_color['rgb']


def getRandomHex():
    return random_color['hex']


def getColor(color):
    try:
        return {color: colorBase[color]}
    except KeyError:
        return {'black': colorBase['black']}


def getRGB(color):
    """
    return:  RGB value if color is found else return black color
    """
    if color in colorBase.keys():
        return tuple(colorBase[color]['rgb'])
    else:
        return tuple(colorBase['black']['rgb'])


def getHEX(color):
    """
    return:  HEX value if color is found else return black color
    """

    if color in colorBase.keys():
        return colorBase[color]['hex']
    else:
        return colorBase['black']['hex']



# converters
def hue_to_rgb(h):
    r = abs(h * 6.0 - 3.0) - 1.0
    g = 2.0 - abs(h * 6.0 - 2.0)
    b = 2.0 - abs(h * 6.0 - 4.0)
    return saturate(r), saturate(g), saturate(b)


def hsl_to_rgb(h, s, l):
    r, g, b = hue_to_rgb(h)
    c = (1.0 - abs(2.0 * l - 1.0)) * s
    r = (r - 0.5) * c + l
    g = (g - 0.5) * c + l
    b = (b - 0.5) * c + l
    return r, g, b


def hex_to_rgb(color):
    return tuple(int(color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(color):
    if type(color) == list or type(color) == tuple:
        return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])


# validators
def isRGB(color):
    if type(color) in [tuple, list]:
        if len(color) == 3:
            return all([x <= 255 for x in color])
        return False
    raise False


def isHex(color: str, strictmode: bool = False):
    valid_hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

    if color.find('#') != -1:
        color = color.replace('#', '')

    if strictmode:
        condition = len(color) == 6
    else:
        condition = len(color) <= 6

    if type(color) == str and condition:
        return all([h.upper() in valid_hex for h in color])
    return False


def randomPalette():
    with open(file='200color.json', mode='r') as f:
        colorPaletteList = json.loads(f.read())
        return rd.choice(colorPaletteList)


def incrementColor(color: any):
    """
        max rgb value: (255, 255, 255)
        max hex value: #ffffff
    """

    if isinstance(color, str) and isHex(color=color):
        color = hex_to_rgb(color)

    if isRGB(color=color):
        a = color[0]
        b = color[1]
        c = color[2]

        c += 1

        if c == 256:
            c = 0
            b += 1

            if b == 256:
                b = 0

                if 0 < a < 255:
                    a += 1
                else:
                    a = 255
                    b = 255
                    c = 255

        return a, b, c
    return color


if __name__ == '__main__':
    k = incrementColor(color="#ac0000")
    print(k)

