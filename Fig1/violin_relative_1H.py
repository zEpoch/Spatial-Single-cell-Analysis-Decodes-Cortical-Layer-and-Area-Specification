import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import glob
from multiprocessing import Pool
import os


h2_colors = ['#92D050','#99D35B','#A0D666','#ADDB7C','#C8E6A7','#00B0F0','#10B5F1','#D8ADFF','#40C3F4','#7FD6F7','#00B050','#10B55B','#20BA66','#40C37C','#7FD6A7','#FFC000','#FFC820','#FFCF40','#FFD760','#FFDE7F','#209AD2','#FEAAA8','#B870FF','#C8E61B','#FF0000','#CC99FF','#7030A0','#8C57B2','#305496','#4A69A3','#647EB0','#7E93BD','#97A8CA']
h2_types = ['RG1', 'oRG1','Astro-late1','tRG','vRG-late',"EN-ET-SP-early",'EN-ET-SP-P','EN-ET-L5/6','EN-ET-L6-early','EN-ET-SP','IPC-oSVZ','IPC-SVZ-1','IPC-iSVZ', 'IPC-SVZ-2', 'IPC-VZ/SVZ','EN-IZ-1','EN-L2','EN-IZ-2','EN-oSVZ-1','En-oSVZ-2','EN-IT-L6','EN-IT-L4','EN-IT-L4/5','EN-IT-L3/4','EN-IT-L2/3','EC','Astro-1', 'OPC','IN-SST', 'IN-CGE', 'INP-VZ/GE', 'IN-VZ/GE', 'IN-MGE']
h2_dict = dict(zip(h2_types, h2_colors))
sections = ['FB121_GW20-3A', 'FB123_R6-2', 'UMB1117_B-2', 'FB080_BD-230310', 'FB123_R2-2', 'FB080_C-2', 'UMB5900_BA123', 'UMB5900_BA4', 'FB121_5C-rerun', 'UMB5900_BA17', 'FB121_5A-GW20', 'FB080_BA17-3', 'FB080_BA17-2', 'FB080_C', 'UMB1117_FP', 'FB121_GW20-4A', 'FB080_F-lateral', 'FB121_6A-230221', 'UMB1117_FP-2', 'UMB1117_E-dorsal', 'UMB1117_G', 'UMB1117_E-lateral', 'FB080_BA17', 'FB080_F-dorsal4', 'UMB1117_B-1', 'UMB1367_OP', 'UMB5900_BA9', 'UMB5900_BA40', 'UMB5900_BA22', 'FB123_R4', 'FB123_R3', 'FB123_R5', 'FB080_F-ventral', 'FB080_BA17-3_v1_v2', 'FB121_BA17-GW20', 'UMB1367_P']
order = np.load('laminar_violin_order.npy')
dir = os.getcwd()

def make_plot(section):
  os.chdir(dir + '/' + section)
  obs_all = [glob.glob('*obs.csv')][0]
  for i in obs_all:
      print(dir+'-' + i)
      obs = pd.read_csv(i, index_col = 0)
      obs['vz_mz_dist'] = np.sqrt( obs['vz_mz_dist'])
      type_rm = list(obs.value_counts('H2_annotation').index[(obs.value_counts('H2_annotation')<50)])
      if len(type_rm)>0:
        obs1 = obs[~obs.H2_annotation.isin(type_rm)]
        obs2 = obs[obs.H2_annotation.isin(type_rm)]
        #order = list(obs.groupby('H2_annotation').aggregate('median').sort_values(by='vz_mz_dist').index)
        plt.figure(figsize=(30,15));
        plot = sns.violinplot(x='H2_annotation', y='vz_mz_dist', hue='H2_annotation', data=obs1, order=order, palette=h2_dict, density_norm='width', inner = None, dodge=False, cut=0);
        plot.legend().remove(); plt.xticks(rotation=90, fontsize=12); plt.yticks(fontsize=12); plot.set(xlabel=None); plot.set_ylabel('Laminar Depth', fontsize=20); plt.ylim(0,1);
        sns.stripplot(x='H2_annotation', y='vz_mz_dist', hue='H2_annotation', data=obs2, order=order, palette=h2_dict);
        plt.savefig(i.split('_')[0] + '_violin.png', dpi=500, bbox_to_inches = 'tight')
      else:
        #order = list(obs.groupby('H2_annotation').aggregate('median').sort_values(by='vz_mz_dist').index)
        plt.figure(figsize=(30,15));
        plot = sns.violinplot(x='H2_annotation', y='vz_mz_dist', hue='H2_annotation', data=obs, order=order, palette=h2_dict, density_norm='width', inner = None, dodge=False, cut=0);
        plot.legend().remove(); plt.xticks(rotation=90, fontsize=12); plt.yticks(fontsize=12); plot.set(xlabel=None); plot.set_ylabel('Laminar Depth', fontsize=20); plt.ylim(0,1); plt.savefig(i.split('_')[0] + '_violin.png', dpi=500, bbox_to_inches = 'tight')
        
          
def main():
  with Pool(12) as pool:
    pool.map(make_plot, sections)

if __name__=="__main__":
    main()
