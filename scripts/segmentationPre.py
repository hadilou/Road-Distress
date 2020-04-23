
"""
@author Kayode H. ADJE
		kaadje@ttu.ee
"""
from gaps_dataset import gaps
import numpy as np
from PIL import Image
import os
import glob

test_img_link = "../Dataset/v2/segmentation/images/_cam12_1431182332579_000743.jpg"
test_folder = "../Dataset/test"
def crop(im,desiredHeight,desiredWidth):
    """ 
    Crop given image to desired height and width

    """
    imgwidth, imgheight = im.size
    for i in range(imgheight//desiredHeight):
        for j in range(imgwidth//desiredWidth):
            box = (j*desiredWidth, i*desiredHeight, (j+1)*desiredWidth, (i+1)*desiredHeight)
            out = im.crop(box)
            #out.show()
            yield out

im = Image.open(test_img_link)

crop(im,320,240)







