"""@author Kayode H. ADJE
		kaadje@ttu.ee
"""

import cv2
from PIL import Image
import numpy as np

test_path = "../InputTest/_cam11_1431264434462_000256_5_2.png"
sum = 0
if test_path.lower().endswith((".jpg",".png",".PNG",".JPG",".jpeg",".JPEG")):
    try:
        im = Image.open(test_path)
        m = np.matrix(im)
        width,height = m.shape
        for i in range(width):
            for j in range(height):
                if m[i,j]==0: 
                    print([i,j])
                    sum+=1
        h,w = im.size
        print(im.size)
        print(sum/(320*180)*100)
    except Exception as e:
        print(e)
else:#file not image ignore
    pass

