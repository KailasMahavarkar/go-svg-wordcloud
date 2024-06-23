from PIL import Image
import numpy as np
import glob
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
import skimage.filters
import os

rootPath = os.path.dirname(os.path.abspath(__file__))
# imagePath = os.path.join(rootPath, "06-junk-before.png")
imagePath = os.path.join(rootPath, "IMG_20171229_135723.jpg")


class MaskReal:
    def __init__(self, filename) -> None:
        self.mask = None

        # read the original image, converting to grayscale on the fly
        self.image = skimage.io.imread(filename, as_gray=True)
        self.sigma_image = None

    def sigmaConverter(self):
        # blur before thresholding
        blurred_image = skimage.filters.gaussian(self.image, sigma=1)

        # perform automatic thresholding to produce a binary image
        t = skimage.filters.threshold_otsu(blurred_image)
        if t < 0.8:
            t = 0.8
        binary_mask = blurred_image > t

        # return the binary mask image
        self.sigma_image = binary_mask

        return Image.fromarray(self.sigma_image)

    def display(self):
        # display image matplotlib
        fig, ax = plt.subplots()
        plt.imshow(self.sigma_image, cmap='gray')
        plt.show()

    def save(self):
        # save image
        Image.fromarray(self.sigma_image).save(
            os.path.join(rootPath, "temp.jpg"))


if __name__ == '__main__':

    def resizer(image, desired_width=800, desired_height=800):

        if not desired_height:
            desired_height = 1000

        if not desired_width:
            desired_width = 1000

        width, height = image.size
        resized = image.resize(
            (
                width - (width // 10),
                height - (height // 10)
            ),
            Image.ANTIALIAS
        )

        if resized.size.width > desired_width or resized.size.height > desired_height:
            resizer(
                image=resized,
                desired_width=desired_width,
                desired_height=desired_height
            )

        return resized


    def centerImages(outer, inner):
        if not outer:
            outer = Image.new(mode='RGB', size=(1000, 1000), color='white')

        if not inner:
            inner = Image.new(mode='RGB', size=(500, 500), color='black')

        outer_width, outer_height = outer.size
        inner_width, inner_height = inner.size

        inner.show()

        cordinates = (
            outer_width - inner_width) // 2,  (outer_height - inner_height) // 2

        outer.paste(inner, cordinates)
        return outer

    # outer_image = False
    innner_image = MaskReal(filename=imagePath).sigmaConverter()

    resizer(innner_image)

    # centerImages(
    #     False, innner_image
    # ).show()

    # innner_image.show()
