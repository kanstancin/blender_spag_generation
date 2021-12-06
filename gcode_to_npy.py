import pandas as pd
import numpy as np

def parse(x):
    row = [None, None, None]
    for val in x:
        if val == None: continue
        if val[0] == "X": row[0] = val[1:]
        elif val[0] == "Y": row[1] = val[1:]
        elif val[0] == "Z": row[2] = val[1:]
    return pd.Series(row, index=['X', 'Y', 'Z'])
    
def cont_check(arr1, arr2):
    arr_out = np.zeros(len(arr1))
    for val in arr2:
        arr_out = np.logical_or(arr_out , (arr1 == val))
    return arr_out

def space_z(arr):
    return np.linspace(0,30,len(arr))
       
data = pd.read_csv("gcodes/M_Wanne.gcode", header=None)
data = data[0].str.split(" ", expand=True)
print(data.head())

#data = data.apply(parse, axis=1)
#data.to_csv('gcode.csv')
data = pd.read_csv('gcode.csv')
z_levels = data.Z.unique()
z_levels_trim = z_levels[len(z_levels)//2:len(z_levels)//2+5]
data = data.fillna(value=None, method='ffill', axis=0)
data = data[cont_check(data.Z, z_levels_trim)]

data.Z = space_z(data.Z)
np.save("gcode.npy",data)
print(len(data.Z.unique()))
