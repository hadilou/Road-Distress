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

def non_void_percentage(mask):
    """
    Calculate percentage of non void pixels(!= 1) in a mask

    Parameter
    -----
    mask: Image,source image

    Returns
    -----
    p: float, percentage of non void pixels
    """
    width,height = mask.shape
    # boolean matrix , faster, one of the comparer should be numpy matrix at least 
    # a void pixel is a zero pixel
    x,_y = (mask == 0).nonzero()
    return (x.shape[0] / (width * height) ) * 100.0

def main(input_dir,output_dir,threshold):
    """
    Main function
    """
        #make sure directory exists
    if (os.path.isdir(output_dir)):
        shutil.rmtree(output_dir)
        os.mkdir(output_dir)
    else:
        os.mkdir(output_dir)

    #browse inputdir , calculate % of non void pixels
    for file in os.listdir(input_dir):
        if file.lower().endswith((".jpg",".png",".PNG",".JPG",".jpeg",".JPEG")):
            try:
                im = Image.open(os.path.join(input_dir,file))
                filename = substract(im.filename,os.path.dirname(im.filename))
                m = np.array(im)
                p = non_void_percentage(np.array(m))
                print("Percentage of void is "+str(p))
                if (p <= threshold):#save mask and do nothing to corresponding training img
                    #save mask
                    path = output_dir+ filename
                    print("Saving to ",format(path))
                    cv2.imwrite(path,m)
                    
                else:
                    #percentage less than threshold, remove corresponding img from  images folder
                    path = os.path.dirname(input_dir)+"/images"
                    f_name,_f_extension = os.path.splitext(im.filename)
                    f_name = substract(f_name,os.path.dirname(f_name))
                    print("Removing "+str(filename)+" from "+ str(path))
                    path =  path+f_name + ".jpg"
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
    ap.add_argument("-i","--inputdir",required=True,help="Path to input directory")
    ap.add_argument("-o","--outputdir",required=True,help="Path to output directory")
    ap.add_argument("-t","--threshold",required=False,help="Desired non void threshold, type =float, default = 80")

    args = vars(ap.parse_args())
    input_dir = args["inputdir"]
    output_dir = args["outputdir"]
    threshold = args["threshold"]
    main(input_dir,output_dir,threshold=80.0)
    