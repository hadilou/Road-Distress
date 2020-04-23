import cv2
import numpy as np
import os
from tqdm import tqdm
import shutil
import math
import random

# Make nondefect segment generation repeatable
random.seed(2323)

# Path to where the images with .defect.mask.png and .cut.mask_v2.png are stored
# NB! DO NOT, I repeat, DO NOT choose POST_SRC_FOLDER the same as PRE_SRC_FOLDER
# This is because it is CLEARED of ALL FILES on every run
# NEVER choose POST_SRC_FOLDER as folder that already contains some data, otherwise you will lose it!
PRE_SRC_FOLDER = "C:\\work\\defects\\data\\ortho_masks\\ALL_DATA_ADD"
PNG_FOLDER = "C:\\work\\defects\\data\\segs_336_thr0.5" # NEW FOLDER!

# Some file naming conventions
ORIG_IMG = ".jpg"
CUT_MASK_V1 = ".cut.mask.png"
CUT_MASK_V2 = ".cut.mask_v2.png"
DEFECT_MASK = ".defectsfixed.png"
DILATION_MASK = '.lmask.png'

USE_DILATION_MASK = True

NEEDED_CIRCLE_MASK = True

THR_IMAGE = 0.5 # Useful pixel ratio
THR_DEFECT = 0.01 # Percentage of pixels needed to be defected/dilate defected to add them to the segment set
SEG_WH = (336, 336) # Segment size
INVERT_ROADMASK = False

def create_circular_mask(h, w, center=None, radius=None):
    mask_array = np.zeros((h,w), np.uint8)
    if center is None: # use the middle of the image
        center = [int(w/2), int(h/2)]
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    mask = (mask*255).astype(np.uint8)
    #mask[mask] = 1
    #print(mask)
    return mask

# Percent of nonblack pixels in given rectangle
def seg_get_nonblack_pixel_percentage(mask, ctuple):
    x, y, w, h = ctuple
    seg = mask[y:y + h, x:x + w]
    #print(cv2.countNonZero(seg) / (w * h))
    return cv2.countNonZero(seg) / (w * h)

def seg_preparse_image(mask, segwh, thr, roadmask):
    seg_width, seg_height = segwh
    h, w = mask.shape
    if seg_width > w or seg_height > h:
        print("Segment size is larger than the image: cannot proceed")
        return

    ovrlap = 2
    # Number of segments per line and row
    numSegsX = int(math.floor(w / seg_width))*ovrlap
    numSegsY = int(math.floor(h / seg_height))*ovrlap

    # Segment list
    seg_list = []

    # Segmentation should be done in four steps:
    # 1. Top to bottom, left to right
    # 2. Rightmost boundary: take all segments from the right-end pixel along the vertical (top to bottom)
    # 3. Bottommost boundary: take all segments from the bottom-end pixel along the horizontal (left to right)
    # 4. Final segment: the last segment located in the bottom right.
    # Unless masked, these regions will be overrepresented slightly.

    # Step 1
    # for sy in range(numSegsY):
    #     for sx in range(numSegsX):
    #         px, py, pw, ph = (sx * seg_width, sy * seg_height, seg_width, seg_height)
    #         if seg_get_nonblack_pixel_percentage(mask, (px, py, pw, ph)) >= thr:
    #             seg_list.append((px, py, pw, ph))
    for sy in range(numSegsY):
        for sx in range(numSegsX):
            px, py, pw, ph = (math.floor(sx * seg_width/ovrlap), math.floor(sy * seg_height/ovrlap), seg_width, seg_height)
            if (seg_get_nonblack_pixel_percentage(roadmask, (px, py, pw, ph)) >= thr) and (seg_get_nonblack_pixel_percentage(mask, (px, py, pw, ph)) >= THR_DEFECT):
                seg_list.append((px, py, pw, ph))

    # Step 2
    # for sy in range(numSegsY):
    #     px, py, pw, ph = (w - seg_width, sy * seg_height, seg_width, seg_height)
    #     if seg_get_nonblack_pixel_percentage(mask, (px, py, pw, ph)) >= thr:
    #         seg_list.append((px, py, pw, ph))

    # # Step 3
    # for sx in range(numSegsX):
    #     px, py, pw, ph = (sx * seg_width, h - seg_height, seg_width, seg_height)
    #     if seg_get_nonblack_pixel_percentage(mask, (px, py, pw, ph)) >= thr:
    #         seg_list.append((px, py, pw, ph))

    # # Step 4
    # px, py, pw, ph = (w - seg_width, h - seg_height, seg_width, seg_height)
    # if seg_get_nonblack_pixel_percentage(mask, (px, py, pw, ph)) >= thr:
    #     seg_list.append((px, py, pw, ph))

    return seg_list

##### SCRIPT BEGINS HERE

# Create the new dir as needed
if os.path.exists(PNG_FOLDER):
    shutil.rmtree(PNG_FOLDER)
    os.makedirs(PNG_FOLDER)
else:
    os.makedirs(PNG_FOLDER)

# Files for prescreening
all_prescr_files = os.listdir(PRE_SRC_FOLDER)

files_with_defects_noext = []
for fil in all_prescr_files:
    if ORIG_IMG in fil:
        # Some grabcut bad apples filtered out
        #if '074118' not in fil:
        files_with_defects_noext.append(fil.split(".")[0])

if NEEDED_CIRCLE_MASK:        
    circlemask = create_circular_mask(4096, 4096, radius=1500)
    circlemask = cv2.cvtColor(circlemask, cv2.COLOR_GRAY2RGB)

# Now we start processing
for n in tqdm(range(len(files_with_defects_noext))):
    # File name
    myfile = files_with_defects_noext[n]
    print(myfile)

    # Load the original image
    img = cv2.imread(PRE_SRC_FOLDER + os.sep + myfile + ORIG_IMG)
    


    # Check which mask to load
    road_mask = None
    if os.path.isfile(PRE_SRC_FOLDER + os.sep + myfile + CUT_MASK_V2):
        road_mask = cv2.imread(PRE_SRC_FOLDER + os.sep + myfile + CUT_MASK_V2)
    elif os.path.isfile(PRE_SRC_FOLDER + os.sep + myfile + CUT_MASK_V1):
        road_mask = cv2.imread(PRE_SRC_FOLDER + os.sep + myfile + CUT_MASK_V1)
    else:
        print('No road mask found!')

    if NEEDED_CIRCLE_MASK:
        road_mask[np.where((circlemask == [0, 0, 0]).all(axis=2))] = [0, 0, 0]
    #else:
        # Create a 1500px circle mask
    #    h, w = img.shape[:2]
    #    road_mask = create_circular_mask(h, w, radius=2000)
        #road_mask = cv2.cvtColor(road_mask, cv2.COLOR_GRAY2BGR)

    # Load the defect mask
    if os.path.isfile(PRE_SRC_FOLDER + os.sep + myfile + DEFECT_MASK):
        dmask = cv2.imread(PRE_SRC_FOLDER + os.sep + myfile + DEFECT_MASK)
    else:
        dmask = np.zeros([4096,4096,3], dtype=np.uint8)

    if USE_DILATION_MASK == True:
        # Load the dilated mask
        if os.path.isfile(PRE_SRC_FOLDER + os.sep + myfile + DILATION_MASK):
            mask_dilated = cv2.imread(PRE_SRC_FOLDER + os.sep + myfile + DILATION_MASK)
        #mask = cv2.bitwise_and(mask, mask_dilated)
        else:
            mask_dilated = dmask
            print('Dilation mask for ' + myfile + ' not found, using defect mask instead' )



    if INVERT_ROADMASK == True:
        img[road_mask] = 0
        dmask[road_mask] = 0
    else:
        img[np.where(road_mask == 0)] = 0
        dmask[np.where(road_mask == 0)] = 0
        mask_dilated[np.where(road_mask == 0)] = 0
    # Make masks greyscale
    mask_dilated = cv2.cvtColor(mask_dilated, cv2.COLOR_BGR2GRAY)
    def_mask = cv2.cvtColor(dmask, cv2.COLOR_BGR2GRAY)
    road_mask = cv2.cvtColor(road_mask, cv2.COLOR_BGR2GRAY)
    #if len(road_mask.shape) > 1:
    #    road_mask = cv2.cvtColor(road_mask, cv2.COLOR_BGR2GRAY)
    # Only use the masked area of img
    #img = img[np.where((road_mask >= 1).all(axis=2))] = 0
    #pos = np.where(road_mask == 0)
    #img[pos] = 0

    # First, clip defect mask to actual mask
    #dmask[np.where((road_mask == 0).all(axis=2))] = 0

    # Now we compile the list of all segments
    segs = seg_preparse_image(mask_dilated, SEG_WH, THR_IMAGE, road_mask)


    # Store defects
    for k in range(len(segs)):
        px, py, pw, ph = segs[k]
        now_seg = img[py:py + pw, px:px + pw]
        now_seg_defmask = def_mask[py:py + pw, px:px + pw]
        cv2.imwrite(PNG_FOLDER + os.sep + os.sep
                    + myfile + ("_%04d" % k) + ".png", now_seg)
        cv2.imwrite(PNG_FOLDER + os.sep + os.sep
                    + myfile + ("_%04d" % k) + '_groundtruth' + ".png", now_seg_defmask)