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
    Convert and save numpy matrix to images

    Parameters
    -------
    chunk: Numpy matrix, chunk of data to convert and save

    chunkid: Int, index of chunk in input folder

    output_dir: String, path for saving chunk images
    """
    desiredFormat = ".png"
    #denormalize chunk
    denormalized = denormalize(chunk,255,0,127.5,1,-1)#denormalized chunk
    #convert greyscale to RGB
    imgs=cv2.merge([denormalized, denormalized, denormalized])
    #print(imgs.shape)
    for i in range(chunk.shape[0]):
        img = cv2.cvtColor(imgs[i][0], cv2.COLOR_RGB2BGR)#opencv  sees bgr  as rgb
        temp =os.path.join(output_dir,"label_"+str(chunkid))
        if (os.path.isdir(temp)):#making sure label_i folder exists
            pass
        else:
            os.mkdir(temp)
        #saving to output_dir
        temp = output_dir + "/label_"+str(chunkid)
        path = os.path.join(temp,"img"+str(i+1)+desiredFormat)
        print("Saving to :"+str(path))

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
    chunkid = int((len([file for file in os.listdir(input_dir)])-3)/2-1)
    
    print(chunkid)
    for file in os.listdir(input_dir):
        if file.lower().endswith(("x.npy")):
            mat2image(np.load(input_dir+str("/")+str(file)),chunkid,output_dir)
            chunkid-=1
        elif file.lower().endswith(("y.npy")):
            #copy _y.npy file to corresponding path
            temp =os.path.join(output_dir,"label_"+str(chunkid))
            if (os.path.isdir(temp)):#making sure label_i folder exists
                pass
            else:
                os.mkdir(temp)
            path = os.path.join(input_dir,file)
            print("Copying "+str(path)+ str(" to ")+output_dir)
            shutil.copy(path,temp)

            
            

if __name__=='__main__':
    #Parsing arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--inputdir",required=True,help="Path to input directory")
    ap.add_argument("-o","--outputdir",required=True,help="Path to output directory")

    args = vars(ap.parse_args())
    input_dir = args["inputdir"]
    output_dir = args["outputdir"]
    main(input_dir,output_dir)    