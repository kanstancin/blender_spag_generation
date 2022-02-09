import numpy as np
import cv2 as cv
import os
from multiprocessing import Pool
from glob import glob

def crop_frg(im):
        non_zero = im[:, :, 3].nonzero()
        i_min, i_max = [np.min(non_zero[0]), np.max(non_zero[0])]
        j_min, j_max = [np.min(non_zero[1]), np.max(non_zero[1])]
        return im[i_min:i_max, j_min:j_max]

def crop_imgs(i, im_path_in):
	if i > 1910: 
					
		try:
			img = cv.imread(im_path_in,cv.IMREAD_UNCHANGED)
			img = crop_frg(img)
		except Exception as e:
			print(f"ERROR {e}")	
			return 1			
		path_out = "/home/cstar/workspace/blender_spag_generation/pictures_cropped"	
		im_name = os.path.basename(im_path_in)
		im_path_out = os.path.join(path_out, im_name)
		cv.imwrite(im_path_out, img)
		print(f"processed image: {i}")
		return 0
	
if __name__ == "__main__":
	path_in = "/home/cstar/workspace/blender_spag_generation/pictures"
	path_out = "/home/cstar/workspace/blender_spag_generation/pictures_cropped"
	files = glob(os.path.join(path_in, "*"))
	pool = Pool()                         # Create a multiprocessing Pool
	pool.starmap(crop_imgs, enumerate(files)) 
		
		
		

