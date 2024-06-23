import svgwrite
import requests


def text_to_svg(text, bg_color, text_color, font_size,  font_family):
    # check if the user-specified font family is available on Google Fonts
    font_url = f"https://fonts.googleapis.com/css?family={font_family.replace(' ', '+')}"
    r = requests.get(font_url)
    if r.status_code != 200:
        # if the user-specified font family is not available, use Product Sans as fallback
        font_family = "Product Sans"
    dwg = svgwrite.Drawing(size=(1000, 1000))
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill=bg_color))
    text_element = dwg.text(text, insert=(500, 500), text_anchor="middle", alignment_baseline="middle",
                            fill=text_color, font_size=font_size, font_family=font_family)
    dwg.add(text_element)
    dwg.save()


text_to_svg("MewAconite123", "black", "white", 200, "Product Sans")
