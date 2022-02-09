import sys
path = "/home/cstar/workspace/blender_spag_generation/"
#from joblib import Parallel, delayed

if path not in sys.path:
    sys.path.append(path)
from imp import reload 
import bpy_funcs_
reload(bpy_funcs_) 
print(sys.version)
import random
import numpy as np
from math import floor
from glob import glob
import os

class RandomSpag: # gcode # random sp 
    def __init__(self, gcode_dir, out_path="",\
                  s_x=[0.1, 1], s_y=[0.1, 1], s_z=[0.3, 1.5], sparse_rate=[3, 7],\
                            space_z=[0.5, 3], \
                  number_cuts=[10,100], resize=[1, 3], seed=[0,10000], \
                  bevel_depth=[0.005,0.02], diffuse_color=[0,1], \
                  num_lights=[5, 10], light_energy=[80, 300], \
                  gcode_prob=0.8, \
                  num_rotation_steps=3, save=False, h_range=[30,80], bckg_transparent=True):
        self.gcode_dir = gcode_dir
        self.s_x = s_x
        self.s_y = s_y 
        self.s_z = s_z
        self.sparse_rate = sparse_rate
        self.space_z = space_z
        self.number_cuts = number_cuts 
        self.resize = resize 
        self.seed = seed
        self.bevel_depth = bevel_depth 
        self.diffuse_color = diffuse_color
        self.num_lights = num_lights
        self.light_energy = light_energy
        self.gcode_prob = gcode_prob
        self.num_rotation_steps = num_rotation_steps
        self.save = save
        self.bckg_transparent = bckg_transparent
        self.h_range = h_range
        self.state = {"choice_func":""}
                
    def __call__(self, image_file):
        s_x = s_y = rand_gauss_range(self.s_x, mu=0.0, sigma=0.3)
        s_z = rand_gauss_range(self.s_z, mu=0.0, sigma=0.3)
        sparse_rate = rand_gauss_range(self.sparse_rate, mu=0.3, sigma=0.3, is_real=False)
#        sparse_rate = rand_gauss_range(self.sparse_rate, mu=0.1, is_real=False)
        space_z = rand_gauss_range(self.space_z, mu=0)
        
        number_cuts = rand_unif_range(self.number_cuts, is_real=False)
        resize = rand_populate_arr(self.resize, rand_unif_range, 3)
        #resize = [rand_unif_range(resize),rand_unif_range(resize),rand_unif_range(resize)]
        seed = rand_unif_range(self.seed, is_real=False)
        
        bevel_depth = rand_unif_range(self.bevel_depth)
        diffuse_color = rand_populate_arr(self.diffuse_color, rand_unif_range, 3)
        diffuse_color.append(1)
        
        num_lights = rand_unif_range(self.num_lights, is_real=False)
        light_energy = rand_unif_range(self.light_energy)
        
        weights = np.array([self.gcode_prob, 1-self.gcode_prob])*100
        print(weights)
        self.state["choice_func"] = random.choices([1, 2], weights=weights)[0]
        print(self.state["choice_func"])
        if self.state["choice_func"] == 1:
            bpy_funcs_.add_spline_from_gcode(image_file,s_x=s_x, s_y=s_y, s_z=s_z, \
                                                sparse_rate=sparse_rate,\
                                                space_z=space_z)
        elif self.state["choice_func"] == 2:
            bpy_funcs_.create_random_sp(number_cuts, resize=resize, seed=seed)
        # edit appearence 
        bpy_funcs_.edit_curve_appearence(bevel_depth=bevel_depth, diffuse_color=diffuse_color)

        bpy_funcs_.add_lights(num_lights,light_energy=light_energy, range_l=[3,7])
        
        if self.save:
            bpy_funcs_.save_render2(out_path, num_rotation_steps=self.num_rotation_steps, \
                                    h_range=self.h_range, bckg_transparent=self.bckg_transparent) 
        return self.state
        
def rand_gauss_range(range, mu=0.3, sigma=-1, is_real=True):
    if sigma == -1:
        sigma =  0.6
    mu *= (range[1] - range[0]) 
    sigma *= (range[1] - range[0]) 
    res = range[0] + random.gauss(mu, sigma)
    if res < range[0]: res = range[0]
    elif res > range[1]: res = range[1]
    if is_real:
        return res
    else:
        return floor(res)

def rand_unif_range(range, is_real=True):
    if is_real:
        return random.uniform(range[0],range[1])
    else:
        return random.randint(range[0],range[1])
    
def rand_populate_arr(range_arr, func, size):
    res = [func(range_arr) for i in range(size)]
    return res

def get_filename(arr, i):
    return arr[i % len(arr)]

bpy_funcs_.delete_all_obj()
gcode_dir = "/home/cstar/workspace/blender_spag_generation/gcodes_npy/"
out_path = "/home/cstar/workspace/blender_spag_generation/pictures/"
rand_spag = RandomSpag(gcode_dir, out_path=out_path,\
                  s_x=[0.1, 1], s_y=[0.1, 1], s_z=[0.3, 1.5], sparse_rate=[2, 7],\
                            space_z=[0.5, 3], \
                  number_cuts=[10,100], resize=[1, 3], seed=[0,10000], \
                  bevel_depth=[0.008,0.025], diffuse_color=[0,1], \
                  num_lights=[5, 15], light_energy=[80, 500], \
                  gcode_prob=0.6, \
                  num_rotation_steps=2, save=True, h_range=[10, 80], bckg_transparent=True)

print(np.__version__)
gcode_files = glob(os.path.join(gcode_dir,"*"))
np.random.shuffle(gcode_files)
num_imgs_to_save = 2777
num_gcodes_used = 0
#def gen_spaghetti(arg):

for i in range(num_imgs_to_save):
    bpy_funcs_.delete_all_obj()
    gcode_file = get_filename(gcode_files, num_gcodes_used)
    state = rand_spag(image_file=gcode_file)
    if (state["choice_func"]==1):
        num_gcodes_used += 1
    print(f"\nsaved {i+1} images\n")

#Parallel(n_jobs=-1)(delayed(gen_spaghetti)(i) for i in range(num_imgs_to_save))

#bpy_funcs_.save_render2(out_path, num_rotation_steps=2, h_range=[30, 80])



#bpy_funcs_.delete_all_obj()

#path = "/Users/Kons/Desktop/Mosaic/blender_spag_generation/"
#file = "gcode.npy"
#filename = path + file
## func 1
## s_xy [0.1 1] s_z [0.3 1.5] sparse_rate [1 7] space_z [0.5 3] 
##add_spline_from_gcode(filename,s_x=0.1, s_y=0.1, s_z=0.3, sparse_rate=5, space_z=3)

## func 2
#number_cuts = 100
#resize = [3,3,3]
#seed = 0
## number_cuts [10 100] resize [1 3] seed [0 .. 10000]
#bpy_funcs_.create_random_sp(number_cuts, resize, seed)

## edit appearence 
## bevel_depth [0.005 0.02] # diffuse_color [0 1] 
#bpy_funcs_.edit_curve_appearence(bevel_depth=0.02, diffuse_color=[0.5,0,1,1.0])

#################
## num_lights [5 10] # light_energy [80 300]
#bpy_funcs_.add_lights(5,light_energy=300, range_l=[3,7])

#path_out = "/Users/Kons/Downloads/"
## num_rotation_steps [3]
#bpy_funcs_.save_render(path_out, num_rotation_steps=1)