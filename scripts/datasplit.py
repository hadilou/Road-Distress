import os
import shutil
from PIL import Image
import re
import numpy as np
import cv2


def substract(a,b):
    """Substract two strings
    Parameter
    -----
    a: String, first string to substract from

    b: String, seconf string to substract from a

    Returns
    -----
    out: String, a-b
    """
    out = "".join(a.rsplit(b))
    return out

'''RGB images are here'''
input_dir = "../Dataset/v2/segmentation/images"

'''Binarized and cropped masks are here'''
groundtruth_dir = "../Dataset/v2/groundtruths"

'''RGB images for training will be written here'''
train_output_dir = "../Dataset/v2/train"

'''RGB images for validation will be written here'''
val_output_dir= "../Dataset/v2/valid"

'''Binarized but not cropped masks'''
train_input_dir = "../Dataset/v2/train-binarized"
val_input_dir = "../Dataset/v2/valid-binarized"

desiredWidth = desiredHeight=224
desiredFormat = '.png'

train_names = os.listdir(train_input_dir)
#print(train_names)
valid_names = os.listdir(val_input_dir)


#browse inputdir , calculate % of non void pixels
for file in os.listdir(groundtruth_dir):
    if file.lower().endswith((".jpg",".png",".PNG",".JPG",".jpeg",".JPEG")):
        try:
            f_name,_f_extension = os.path.splitext(file)
            filename = substract(f_name,"_groundtruth")
            #print(filename)
            temp1, temp2 = re.split('_w',filename)
            rawimagename = temp1 + '.jpg'
            maskname = temp1 + desiredFormat
            width0, height0 = re.split('_h',temp2)
            if maskname in train_names:
                src = os.path.join(input_dir,rawimagename)
                output_dir = train_output_dir
            elif maskname in valid_names:
                src = os.path.join(input_dir,rawimagename)
                output_dir = val_output_dir
            if (os.path.isdir(output_dir)):
                pass
            else:
                os.mkdir(output_dir)
            im = Image.open(src)
            box = (int(width0), int(height0), int(width0)+desiredWidth, int(height0)+desiredHeight)
            out = im.crop(box)
            out = np.array(out)
            path = output_dir+'/'+filename+desiredFormat
            print("Saving cropped image to "+path)
            cv2.imwrite(path,out)
        except Exception as e:
            print(e)
    else:#file not image;ignore
        print(str(file)+"  is not an image, skipping")
