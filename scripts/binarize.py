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

def binarize(im,output_dir):
    """
    Convert masks to binary masks, pixels with 0,1 and 7 values are changed to 0 and the others to 1

    Parameters
    -------
    im: Image, image to binarize

    output_dir: String, path to folder where to save the binarized image

    Return 
    ------
    m : numpy.matrix, binarized matrix
    """

    m = np.matrix(im)
    m[m == 0] = 0  #Void is changed to intact
    m[m == 1] = 0  #Intact is intact
    m[m == 2] = 1  #Applied patch is changed to distress
    m[m == 3] = 1  #Pothole is changed to distress
    m[m == 4] = 1  #Inlaid patch is changed to distress
    m[m == 5] = 1  #Open joint is changed to distress
    m[m == 6] = 1  #Crack is changed to distress
    m[m == 7] = 0  #Street inventory is changed to distress

    return m



def main(input_dir,output_dir):
    """
    Main Function
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
                m = binarize(im,output_dir)
                print(np.where(m==1))
                filename = substract(im.filename,os.path.dirname(im.filename))
                path = output_dir+ filename
                print("Saving binarized img to ",format(path))
                cv2.imwrite(path,m)

            except Exception as e:
                print(e)
        else:#file not image;ignore
            pass




if __name__=='__main__':
    #Parsing arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--inputdir",required=True,help="Path to input directory")
    ap.add_argument("-o","--outputdir",required=True,help="Path to output directory")

    args = vars(ap.parse_args())
    input_dir = args["inputdir"]
    output_dir = args["outputdir"]
    main(input_dir,output_dir)

