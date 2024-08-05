import numpy as np
import cv2
import scanpy as sc
import sys
import cv2
from scipy.ndimage.morphology import binary_fill_holes
import warnings
import matplotlib.pyplot as plt
import os
from itertools import compress
import glob
from multiprocessing import Pool
from matplotlib_scalebar.scalebar import ScaleBar


adata = sc.read('merscope_855_no_counts_locs_rotated.h5ad')
adata.obs['sample'][adata.obs['sample']=='GW5900'] = 'UMB5900'

h2_colors = ['#92D050','#99D35B','#A0D666','#ADDB7C','#C8E6A7','#00B0F0','#10B5F1','#D8ADFF','#40C3F4','#7FD6F7','#00B050','#10B55B','#20BA66','#40C37C','#7FD6A7','#FFC000','#FFC820','#FFCF40','#FFD760','#FFDE7F','#209AD2','#FEAAA8','#B870FF','#C8E61B','#FF0000','#CC99FF','#7030A0','#8C57B2','#305496','#4A69A3','#647EB0','#7E93BD','#97A8CA']
h2_types = ['RG1', 'oRG1','Astro-late1','tRG','vRG-late',"EN-ET-SP-early",'EN-ET-SP-P','EN-ET-L5/6','EN-ET-L6-early','EN-ET-SP','IPC-oSVZ','IPC-SVZ-1','IPC-iSVZ', 'IPC-SVZ-2', 'IPC-VZ/SVZ','EN-IZ-1','EN-L2','EN-IZ-2','EN-oSVZ-1','En-oSVZ-2','EN-IT-L6','EN-IT-L4','EN-IT-L4/5','EN-IT-L3/4','EN-IT-L2/3','EC','Astro-1', 'OPC','IN-SST', 'IN-CGE', 'INP-VZ/GE', 'IN-VZ/GE', 'IN-MGE']
h2_dict = dict(zip(h2_types, h2_colors))

def make_plot(sample, region):
    adata1 = adata[(adata.obs['sample']==sample) & (adata.obs.region==region)].copy()
    plot = sc.pl.embedding(adata1, basis="spatial", color = 'H2_annotation', palette=h2_dict, show = False, s=2); plt.axis('off');
    plot.set_aspect('equal');
    handles, labels = plt.gca().get_legend_handles_labels();
    order = [labels.index(i) for i in h2_types];
    plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order], loc = 'center', fontsize=3, ncol = 4, bbox_to_anchor=(0.95,1.05), markerscale=0.5);
    #plot.legend(loc = 'center', fontsize=3, ncol = 3, bbox_to_anchor=(0.95,1), markerscale=0.5);
    plot.get_figure().gca().set_title('');
    scalebar = ScaleBar(1, "um", fixed_value=500, location = 'lower right');
    plot.add_artist(scalebar);
    plt.savefig(sample+'_'+region+'.png', dpi=500); plt.clf()


sections = ['FB121_GW20-3A', 'FB123_R6-2', 'UMB1117_B-2', 'FB080_BD-230310', 'FB123_R2-2', 'FB080_C-2', 'UMB5900_BA123', 'UMB5900_BA4', 'FB121_5C-rerun', 'UMB5900_BA17', 'FB121_5A-GW20', 'FB080_BA17-3', 'FB080_BA17-2', 'FB080_C', 'UMB1117_FP', 'FB121_GW20-4A', 'FB080_F-lateral', 'FB121_6A-230221', 'UMB1117_FP-2', 'UMB1117_E-dorsal', 'UMB1117_G', 'UMB1117_E-lateral', 'FB080_BA17', 'FB080_F-dorsal4', 'UMB1117_B-1', 'UMB1367_OP', 'UMB5900_BA9', 'UMB5900_BA40', 'UMB5900_BA22', 'FB123_R4', 'FB123_R3', 'FB123_R5', 'FB080_F-ventral', 'FB080_BA17-3_v1_v2', 'FB121_BA17-GW20', 'UMB1367_P']

samples = [i.split('_')[0] for i in sections]
regions = [i.split('_')[1] for i in sections]


def main():
  with Pool(12) as pool:
    pool.starmap(make_plot, zip(samples,regions))

if __name__=="__main__":
    main()

