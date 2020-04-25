"""@author Kayode H. ADJE
		kaadje@ttu.ee
"""

import cv2
from PIL import Image
import numpy as np

test_path = "../Dataset/v2/segmentation/test/_cam11_1431182257185_000014.png"

if test_path.lower().endswith((".jpg",".png",".PNG",".JPG",".jpeg",".JPEG")):
    try:
        im = Image.open(test_path)
        m = np.matrix(im)
        width,height = m.shape
        for i in range(width):
            for j in range(height):
                if m[i,j]!=1: 
                    print([i,j])
    except Exception as e:
        print(e)
else:#file not image ignore
    pass
