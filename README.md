
Demo Wep app available for Network output visualisation at https://modeling.onrender.com/     </br>

<a href="https://livettu-my.sharepoint.com/:b:/g/personal/kaadje_ttu_ee/EVsRAjy8HflJo4_8gKhS28wBLakunjvwGpjMHxva7_bxbQ?e=67vmSg">Click to Open Project Report</a> </br>
 


# Updates as 1/05/2020

## a.) Segmentation
The data is  organized as such: </br>
/train/filename_seg{ij}.png </br>
/valid/filename_seg{ij}.png </br>
/groundtruths/filename_seg{00}_groundtruth.png </br>
Please check crop.py


Masks were converted to binary masks, pixels with 0,1 and 7 values are changed to 0(intact) and the others to 1(distres). </br>
Also, there was no need to eliminate void pixels values anymore so eliminate_void.py script became obsolete
Please check binarize.py script.

## b.) Classification
Data is oragnized as follows

/train/label_chunkid/filename.png
/train/label_chunkid/filename.png
...
/valid/label_chunkid/filename.png
/valid/label_chunkid/filename.png
...
/test/label_chunkid/filename.png
/test/label_chunkid/filename.png

Normalized matrix were first denormalized, then converted to RGB from Grayscale before being saved according to the above-mentioned naming
convention



# Updates as 30/04/2020

## a.) Segmentation

gaps.download(login='login',
	output_dir ='../Dataset',
	version=2,
	patchsize='segmentation', 
	debug_outputs =True)


It comprises following folders:

1. Train:       1417 images 
2. Test:        442 images
3. Valid:       51 images
4. Valid test:  500 images
5. Images: contains 58 unlabeled images of road with the resolution of 1920x1080 in jpg format
            contains 2274 labeled images with same resolution. The labeled images correspond to the masks in training, validation, validation test and test datasets. The corresponding masks for these images are in abovementioned folders.

Data partitioning:
Since the resolution for the original images are very high (1920x1080) we partition the images into smaller images (320x180) called segments. The shape of the segments can be modified using the crop.py script.

Void elimination:
Each individual pixel in mask images correspond to one of these classes:
    0 = VOID
    1 = intact road,
    2 = applied patch,
    3 = pothole,
    4 = inlaid patch,
    5 = open joint,
    6 = crack
    7 = street inventory

If more than 80% of a segment is void the segment is simply ignored and corresponding image is removed from the images dataset. The threshold value can be also manipulated using eliminate_void.py script.


# b.) Classification

gaps.download(login='replace_with_your_login',
                    output_dir='desired folder',
                    version=2,
                    patchsize=160,
                    issue='NORMvsDISTRESS_50k')

We used NORMvsDISTRESS_50k with a patch size of 160x160. It consists of following folders:

1. Test: 2 chunks 
2. Train: 10 chunks
3. Valid: 2 chunks
4. Valid test: 2 chunks

A chunk is a numpy array consisting of 5120( except the last chunk of train folder which has 3920) normalized images of 160x160 size within the range of -1 to 1. Also there is a corresponding label for each chunk with a possible value of 0 (intact road) and 1 (distress).

