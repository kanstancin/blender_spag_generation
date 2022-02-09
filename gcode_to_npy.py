import pandas as pd
import numpy as np
import re
from glob import glob

def parse(x):
    row = [None, None, None]
    
    '''
    for val in x:
        if val == None: continue
        if val[0] == "X": row[0] = val[1:]
        elif val[0] == "Y": row[1] = val[1:]
        elif val[0] == "Z": row[2] = val[1:]
    '''
    x = x.to_string()
    coord = ['X', 'Y', 'Z']
    for i, axis in enumerate(coord):
        val = re.findall(f'[{axis}](?:([0-9.]{1,15}))', x)
        if len(val) == 0:
            row[i] = None
        else:
            row[i] = val[0]

    return pd.Series(row, index=['X', 'Y', 'Z'])
    
def cont_check(arr1, arr2):
    arr_out = np.zeros(len(arr1))
    for val in arr2:
        arr_out = np.logical_or(arr_out , (arr1 == val))
    return arr_out

def space_z(arr):
    return np.linspace(0,30,len(arr))

files =  glob("gcodes/*")
for i, file in enumerate(files):
    data = pd.read_csv(file, header=None)
    data = data[0].str.split(" ", expand=True)
    print(file)
    print(data.head())
    data = data.apply(parse, axis=1)
    parts = np.linspace(0.1,0.8,6)
    for j in range(len(parts)):
        print("started "+str(i)+"_"+str(j))
        # data.to_csv('gcode.csv')
        # data = pd.read_csv('gcode.csv')
        z_levels = data.Z.unique()
        z_levels_trim = z_levels[int(len(z_levels)*parts[j]):int(len(z_levels)*parts[j])+5]
        data2 = data.fillna(value=None, method='ffill', axis=0)
        data2 = data2[cont_check(data2.Z, z_levels_trim)]

        data2.Z = space_z(data2.Z)
        np.save("gcodes_npy/"+str(i)+"_"+str(j)+".npy",data2)
