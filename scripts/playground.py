"""
@authors Kayode H. ADJE
		 kaadje@ttu.ee
         Toghrul Aghakishiyev
         toagha@ttu.ee
"""

import cv2
from PIL import Image
import numpy as np

def denormalize(chunk,max,min,mean,to_max,to_min):
    return np.round(chunk*(max-min)/(to_max-to_min)+mean)


test_path = "/Users/allora/Documents/Workspace/RoadDistressProject/Dataset/v2/NORMvsDISTRESS_50k_160/train/chunks_160x160_NORMvsDISTRESS_50k_train_chunk_00_x.npy"

chunk = np.load(test_path)

denormalized = denormalize(chunk,255,0,127.5,1,-1)

im=cv2.merge([denormalized, denormalized, denormalized])

#cv2.imshow(im)
#print(im.shape)
img = cv2.cvtColor(im[0][0], cv2.COLOR_RGB2BGR)
cv2.imwrite("../iii.png",img)