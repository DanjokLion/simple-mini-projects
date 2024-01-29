import pandas as pd
import os

path = 'sladomirCheck/'

files = [f for f in os.listdir(path) if f.endswith('Sale.htm')]

dfs = [] 

for file in files:

    file_path = os.path.join(path, file)

    dfs.append(pd.read_html(file_path)[0])



df_all = pd.concat(dfs, ignore_index=True)

df_all.to_excel('result.xlsx', index=False)