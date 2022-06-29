import os
import numpy as np
import nibabel as nib
from pathlib import Path
import matplotlib.pyplot as plt
import transforms3d 
from scipy import ndimage as ndi
import nibabel.testing
from tqdm import tqdm

data_dir = Path('/home/droopy/Desktop/papa/aimsGH/aims-project/matlab/data')
######################################################################
### load data
######################################################################
sub1 = nib.load(data_dir / 'sub1.nii.gz')
sub1_brain = nib.load(data_dir / 'sub1_brain.nii.gz')
aal3v1 = nib.load(data_dir / 'AAL3v1.nii.gz')

bold_file = sub1
data = sub1.get_fdata()
#print(data.shape)  ## uncomment to see shape of data file
bold_sequence = data
r, c, d, t = bold_sequence.shape
brain_par = 90
averaged_bold_seq = np.zeros((t,brain_par))
atlas = aal3v1.get_fdata()

bold_file = sub1
data = sub1.get_fdata()
bold_sequence = data
r, c, d, t = bold_sequence.shape
brain_par = 90
averaged_bold_seq = np.zeros((t,brain_par))
atlas = aal3v1.get_fdata()

bold_frame = None
temp = None
indices_x = None
indices_y = None

# for all frames
for frame in range(0,t):
    bold_frame = bold_sequence[:,:,:,frame]
    # for all areas
    for b in range(0,brain_par):
        temp = np.zeros((2,1))
        # for all axial plane
        for all_d in range(1,d):
            #find indices
            indices_x,indices_y = np.where(atlas[:,:,all_d]==b)
            #for kk in tqdm(range(0,len(indices_x))):
            for kk in range(0,len(indices_x)):
                try:
                #temp[-1] = bold_frame[indices_x[kk],indices_y[kk],all_d] ## this line can be used
                    if indices_x[kk] < d:
                        temp[-1] = bold_frame[indices_x[kk],indices_y[kk],all_d] ## or this block can be used
                except IndexError:
                    pass
        # remove empty voxels
        temp[temp==0] = None
        #save indices voxels with mean for the specific brain area
        averaged_bold_seq[frame,b] = np.mean(temp)
