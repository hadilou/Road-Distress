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


def denormalize(chunk,max,min,mean,to_max,to_min):
    """
    (De)normalize image from max,min to to_max, to_min

    Parameters
    -------
    chunk: Numpy matrix, Input data to (de)normalize

    max: int, original maximum value

    min: int, original minimum value

    to_max: int, desired maximum value

    to_min: int, desired minimum value

    Returns
    ------
    out: Numpy matrix, (de)normalized numpy matrix
    """
    return np.round(chunk*(max-min)/(to_max-to_min)+mean)


def mat2image(chunk,chunkid,output_dir):
    """

    """
    desiredFormat = ".png"
    denormalized = denormalize(chunk,255,0,127.5,1,-1)#denormalized chunk
    imgs=cv2.merge([denormalized, denormalized, denormalized])

    for i in range(chunk.shape[0]):
        img = cv2.cvtColor(imgs[i][0], cv2.COLOR_RGB2BGR)
        path = output_dir + "/label_"+str(chunkid)+"/img"+str(i)+desiredFormat
        print("Saving to :",format(path))
        cv2.imwrite(path,img)








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
    Main Function
    """
#make sure directory exists
    if (os.path.isdir(output_dir)):
        shutil.rmtree(output_dir)
        os.mkdir(output_dir)
    else:
        os.mkdir(output_dir)

    #browse inputdir , crop and save images
    i = 0
    for file in os.listdir(input_dir):
        if file.lower().endswith(("x.npy")):
            mat2image(np.load(input_dir+str("/")+str(file)),i,output_dir)
            i+=1
        else:#file not _x.npy;ignore
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