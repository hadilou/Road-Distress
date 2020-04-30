
"""
@author Kayode H. ADJE
		kaadje@ttu.ee
"""
from gaps_dataset import gaps
import numpy as np

#Dataset Folder path
dataset_dir = '../Dataset'
#load training dataset info file
train_info = gaps.get_dataset_info(version=2,
                                   patchsize=160,
                                   issue='NORMvsDISTRESS_50k',
                                   subset='train',
                                   datadir='../Dataset')

# load all chunks of training dataset
x_train = []#mat to store x_train
y_train = []#mat to store y_train

for chunk_id in range(train_info['n_chunks']):
    x, y = gaps.load_chunk(
                        chunk_id=chunk_id,
                        version=2,
                        patchsize=160,
                        issue='NORMvsDISTRESS_50k',
                        subset='test',
                        datadir='../Dataset')
    x_train.append(x)
    y_train.append(y)
#convert to np array
x_train = np.array(x_train)
y_train = np.array(y_train)
print("Shape of x_train:"+str(x_train[0]))
#print("Shape of y_train:"+str(y_train.shape))

