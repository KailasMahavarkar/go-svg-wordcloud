import os
from PIL import Image
import requests
from io import BytesIO

file = requests.get("https://a.wattpad.com/cover/143064785-352-k35266.jpg")


img = Image.open(BytesIO(file.content))
rootPath = os.path.abspath(os.path.dirname(__file__))
imgSmall = img.resize((16,16),resample=Image.BILINEAR)
result = imgSmall.resize(img.size,Image.NEAREST)
result.save(os.path.join(rootPath, '../playLab/newImage.jpg'))


name = "file:\\\\\\" + os.path.join(rootPath, '../playLab/newImage.jpg')
print(name.replace("\\", "/"))