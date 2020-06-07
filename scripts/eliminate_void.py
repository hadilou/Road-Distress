"""
@authors Kayode H. ADJE
		 kaadje@ttu.ee
         Toghrul Aghakishiyev
         toagha@ttu.ee
"""
import os
import argparse
import cv2
from PIL import Image
import numpy as np
import shutil

def void_percentage(mask):
    """
    Calculate percentage of  void pixels(== 0) in a mask

    Parameter
    -----
    mask: Image,source image

    Returns
    -----
    p: float, percentage of non void pixels
    """
    width,height = mask.shape
    # boolean matrix , faster computation, one of the comparer should be numpy matrix at least 
    # a void pixel is a zero pixel
    x,_y = (mask == 0).nonzero()
    return (x.shape[0] / (width * height) ) * 100.0

def main(threshold=90.0):
    """
    Main function
    """

    input_dir = "../Dataset/cropped-images" #folder of cropped and binarized images

    groundtruth_dir = "../Dataset/groundtruths2"
    
    train_output_dir = "../Dataset/train2"

    val_output_dir= "../Dataset/valid2"#output after filtering

    train_input_dir = "../Dataset/train" #output after filtering

    val_input_dir = "../Dataset/valid"

    train_names = os.listdir(train_input_dir)
    #print(train_names)
    valid_names = os.listdir(val_input_dir)



    #browse groundtruths , calculate % of non void pixels
    for file in os.listdir(groundtruth_dir):
        if file.lower().endswith((".jpg",".png",".PNG",".JPG",".jpeg",".JPEG")):
            try:
                im = Image.open(os.path.join(groundtruth_dir,file))
                filename = substract(im.filename,os.path.dirname(im.filename))
                m = np.array(im)
                p = void_percentage(np.array(m))
                print("Percentage of intact is "+str(p))
                if (p <= 95):#save mask and do nothing to corresponding training and valid images
                    #save mask
                    f_name,_f_extension = os.path.splitext(file)
                    filename = substract(f_name,"_groundtruth") + ".png"
                    #print(filename)
                    if filename in train_names:#save in train directory
                        dest = os.path.join(train_output_dir,filename)  
                    elif filename in valid_names:#save in validation folder
                        dest = os.path.join(val_output_dir,filename)
                    print("Saving to ",format(dest))
                    im2 = Image.open(os.path.join(input_dir,filename))
                    m2 = np.array(im2)
                    cv2.imwrite(dest,m2)
                    
                else:
                    #percentage of void pixels more than threshold, remove corresponding mask from  groundtruths folder
                    f_name,_f_extension = os.path.splitext(im.filename)
                    f_name = substract(f_name,os.path.dirname(f_name))
                    print("Removing "+str(filename)+" from "+ str(groundtruth_dir))
                    path =  groundtruth_dir+f_name + ".png"
                    os.remove(path)
                    
            except Exception as e:
                print(e)
        else:#file not image;ignore
            print(str(file)+"  is not an image, skipping")

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

if __name__=='__main__':
    #Parsing arguments
    ap = argparse.ArgumentParser()
    #ap.add_argument("-i","--inputdir",required=True,help="Path to input directory")
    #ap.add_argument("-o","--outputdir",required=True,help="Path to output directory")
    ap.add_argument("-t","--threshold",required=False,help="Desired maximum void pixel percentage, type =float, default = 90.0")

    args = vars(ap.parse_args())
    threshold = args["threshold"]
    main(threshold)
    