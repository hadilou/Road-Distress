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


def mat2image(chunk,chunkid,output_dir,file,input_dir):
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
    

    labelname = file.replace("_x","_y")

    label = np.load(input_dir+str("/")+str(labelname))
    folderName = substract(input_dir,os.path.dirname(input_dir))
    folderName = substract(folderName,"/")
    if (os.path.isdir(output_dir + '/' + folderName)):
        pass
    else:
        os.mkdir(output_dir + '/' + folderName)

    if (os.path.isdir(output_dir + '/' + folderName + '/0')):
        pass
    else:
        os.mkdir(output_dir + '/' + folderName + '/0')

    if (os.path.isdir(output_dir + '/' + folderName)):
        pass
    else:
        os.mkdir(output_dir + '/' + folderName)

    if (os.path.isdir(output_dir + '/' + folderName + '/1')):
        pass
    else:
        os.mkdir(output_dir + '/' + folderName + '/1')


    for i in range(chunk.shape[0]):
        img = cv2.cvtColor(imgs[i][0], cv2.COLOR_RGB2BGR)#opencv  sees bgr  as rgb
        #saving to output_dir
        if label[i] == 0:
            path = output_dir +"/"+ folderName + '/' + str(0) + '/' + folderName + '_' + str(chunkid) + "_image_"+str(i+1)+desiredFormat
        else: path = output_dir +"/"+ folderName + '/' + str(1) + '/' + folderName + '_' + str(chunkid) + "_image_"+str(i+1)+desiredFormat     
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
        # shutil.rmtree(output_dir)
        # os.mkdir(output_dir)
        pass
    else:
        os.mkdir(output_dir)
    
    


    #browse inputdir , crop and save images
    chunkid = int((len([file for file in os.listdir(input_dir)])-3)/2)
    
    print(chunkid)
    l = [file for file in os.listdir(input_dir)]
    l.sort()
    l.reverse()
    for file in l:
        if file.lower().endswith(("x.npy")):
            mat2image(np.load(input_dir+str("/")+str(file)),chunkid,output_dir,file,input_dir)
            chunkid-=1
        # elif file.lower().endswith(("y.npy")):
        #     #copy _y.npy file to corresponding path
        #     folder_name = substract(input_dir,os.path.dirname(input_dir))
        #     folder_name=folder_name[1:]
        #     print(folder_name)
        #     des = os.path.join(os.path.dirname(output_dir),"annotation",folder_name)
        #     if os.path.isdir(des):
        #         pass
        #     else:
        #         os.mkdir(des)
        #     inputpath = os.path.join(input_dir,file)
        #     print("Copying "+str(inputpath)+ str(" to ")+output_dir)
        #     shutil.copy(inputpath,des)

            
            

if __name__=='__main__':
    #Parsing arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--inputdir",required=True,help="Path to input directory")
    ap.add_argument("-o","--outputdir",required=True,help="Path to output directory")

    args = vars(ap.parse_args())
    input_dir = args["inputdir"]
    output_dir = args["outputdir"]
    main(input_dir,output_dir)    