"""
@authors Kayode H. ADJE
		 kaadje@ttu.ee
         Toghrul Aghakishiyev
         toagha@ttu.ee
"""
from gaps_dataset import gaps
import numpy as np
from PIL import Image
import os
import glob
import cv2
import argparse
import shutil

def cropAndSave(im,output_dir,desiredHeight=320,desiredWidth=180):
    """ 
    Crop given image to desired height and width and save to desired folder

    Parameters
    -----
    im: Image, directory where images to crop exist

    desiredHeight: int, desired height, default 320

    desiredWidth: int, desired width, default 180

    output_dir: String, path of the folder where to save out to.

    Returns
    ----- 
    out: Image, yield croped image(s)
    """
    imgwidth, imgheight = im.size
    desiredFormat = ".png"
 
    for i in range(imgheight//desiredHeight):
        for j in range(imgwidth//desiredWidth):
            f_name,_f_extension = os.path.splitext(im.filename)
            f_name = substract(f_name,os.path.dirname(f_name))
            box = (j*desiredWidth, i*desiredHeight, (j+1)*desiredWidth, (i+1)*desiredHeight)
            out = im.crop(box)
            out = np.array(out)
            temp = substract(output_dir,os.path.dirname(output_dir))
            if (temp=="/groundtruths"): #add '_groundtruth' to the path
                path = output_dir+f_name+'_seg'+str(i)+str(j)+"_groundtruth"+str(desiredFormat)
            else :
                path = output_dir+f_name+'_seg'+str(i)+str(j)+str(desiredFormat)
            print("Saving cropped image to "+path)
            cv2.imwrite(path,out)
            #yield out

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

def main(input_dir,output_dir):
    """
    Main function
    """
    #make sure directory exists
    if (os.path.isdir(output_dir)):
        shutil.rmtree(output_dir)
        os.mkdir(output_dir)
    else:
        os.mkdir(output_dir)

    #browse inputdir , crop and save images
    for file in os.listdir(input_dir):
        if file.lower().endswith((".jpg",".png",".PNG",".JPG",".jpeg",".JPEG")):
            try:
                im = Image.open(os.path.join(input_dir,file))
                cropAndSave(im,output_dir) 
            except Exception as e:
                print(e)
        else:#file not image;ignore
            pass
    
if __name__=='__main__':
    #Parsing arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--inputdir",required=True,help="Path to input directory")
    ap.add_argument("-o","--outputdir",required=True,help="Path to output directory")
    ap.add_argument("-w","--width",required=False,help="Desired Width, default 320")
    ap.add_argument("-l","--height",required=False,help="Desired Height, default 180")

    args = vars(ap.parse_args())
    input_dir = args["inputdir"]
    output_dir = args["outputdir"]
    desired_h = args["height"]
    desired_w = args["width"]
    #main function call
    main(input_dir,output_dir)





