from joblib import Parallel, delayed
import pandas as pd
import numpy as np
import re
from glob import glob

def parse(x):
    row = [None, None, None]
    x = x.split(" ")
    for val in x:
        if val == None: continue
        if val[0] == "X": row[0] = val[1:]
        elif val[0] == "Y": row[1] = val[1:]
        elif val[0] == "Z": row[2] = val[1:]
    return row
    
def cont_check(arr1, arr2):
    arr_out = np.zeros(len(arr1))
    for val in arr2:
        arr_out = np.logical_or(arr_out , (arr1 == val))
    return arr_out

def space_z(arr):
    return np.linspace(0,30,len(arr))

files =  glob("gcodes/*")
for i, filename in enumerate(files):
    if i >= 4*len(files)/7 and i <= 5*len(files)/7:
        print(filename)
        lines = []
        with open(filename) as f:
            lines = f.readlines()
            print(f'file: {filename} has {len(lines)} lines')

        result_file = []
        for line in lines:
            result = parse(line)
            result_file.append(result)

        print(len(result_file))
        data  = pd.DataFrame(result_file, columns=['X', 'Y', 'Z'])
        print(data.head())
        parts = np.linspace(0.1,0.8,6)
        for j in range(len(parts)):
            file_dir = filename.split('/')
            new_name = file_dir[1].split('.')
            print("started "+new_name[0]+"_"+str(j))
            # data.to_csv('gcode.csv')
            # data = pd.read_csv('gcode.csv')
            z_levels = data.Z.unique()
            z_levels_trim = z_levels[int(len(z_levels)*parts[j]):int(len(z_levels)*parts[j])+5]
            data2 = data.fillna(value=None, method='ffill', axis=0)
            data2 = data2[cont_check(data2.Z, z_levels_trim)]

            data2.Z = space_z(data2.Z)
            print(data2.head())
            np.save("gcodes_npy/"+new_name[0]+"_"+str(j)+".npy",data2)

    


