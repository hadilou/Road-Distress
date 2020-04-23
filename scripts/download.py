
"""
@author Kayode H. ADJE
		kaadje@ttu.ee
"""
from gaps_dataset import gaps

gaps.download(login='gapsro2s;i2A*7',
	output_dir ='Dataset',
	version=2,
	patchsize=160,
	issue='NORMvsDISTRESS_50k',
	debug_outputs =True)
