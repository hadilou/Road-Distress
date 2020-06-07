import os
import shutil
from PIL import Image


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

input_dir = "../Dataset/cropped-images"

train_output_dir = "../Dataset/train"

val_output_dir= "../Dataset/valid"

train_input_dir = "../Dataset/train0"
val_input_dir = "../Dataset/valid0"



train_names = os.listdir(train_input_dir)
#print(train_names)
valid_names = os.listdir(val_input_dir)


#browse inputdir , calculate % of non void pixels
for file in os.listdir(input_dir):
    if file.lower().endswith((".jpg",".png",".PNG",".JPG",".jpeg",".JPEG")):
        try:
            f_name,_f_extension = os.path.splitext(file)
            filename = substract(f_name,"_groundtruth") + ".png"
            #print(filename)
            if filename in train_names:
                src = os.path.join(input_dir,filename)
                dest = os.path.join(train_output_dir,filename)
                print("Copying "+str(src)+" to "+str(dest))
                shutil.copyfile(src, dest)
            elif filename in valid_names:
                src = os.path.join(input_dir,filename)
                dest = os.path.join(val_output_dir,filename)
                print("Copying "+str(src)+" to "+str(dest))
                shutil.copyfile(src, dest)

        except Exception as e:
            print(e)
    else:#file not image;ignore
        print(str(file)+"  is not an image, skipping")

