
"""
@author Kayode H. ADJE
		kaadje@ttu.ee
"""
from gaps_dataset import gaps

#issues  possible values: ['NORMvsDISTRESS', 'NORMvsDISTRESS_50k', 'ZEB_50k']
# possible values: [None, 'train', 'valid', 'valid-test', 'test']
# possible values: [64, 96, 128, 160, 192, 224, 256]

gaps.download(login='gapsro2s;i2A*7',
	output_dir ='../Dataset',
	version=2,
	patchsize='segmentation', 
	debug_outputs =True)
