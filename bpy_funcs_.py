from bpy import context, data, ops    
from math import radians                
import bpy
import random

from mathutils import Vector
import numpy as np
import statistics as stat

from math import *
from mathutils import *
import os

def center_obj(arr):
        arr = np.array(arr)
        x_avg = stat.mean(arr[:,0])
        y_avg = stat.mean(arr[:,1])
        arr[:,0] -= x_avg
        arr[:,1] -= y_avg
        return arr.tolist()

def randomize_xyz(p, s_x, s_y, s_z):
            p[0] += random.gauss(0,s_x)
            p[1] += random.gauss(0,s_y)
            p[2] += random.gauss(0,s_z)
            return p
        
def stretch_z(arr, space):
    return np.linspace(0,space,len(arr))
        
def add_spline_from_gcode(filename, s_x=0.1, s_y=0.1, s_z=0.3, sparse_rate=10, space_z=3):
    coords_list = np.load(filename,  allow_pickle=True) 
    coords_list = coords_list.astype(np.float)
    print(coords_list)
    print(coords_list.dtype)      
    print(coords_list.shape)
    coords_list = np.array(coords_list[::sparse_rate] / 10)
    print(coords_list.shape)
    coords_list[:,2] = stretch_z(coords_list[:,2],space_z)
    coords_list = coords_list.tolist()
    coords_list = center_obj(coords_list) 

    # make a new curve
    crv = bpy.data.curves.new('crv', 'CURVE')
    crv.dimensions = '3D'

    # make a new spline in that curve
    spline = crv.splines.new(type='NURBS')

    # a spline point for each point
    spline.points.add(len(coords_list)-1) # theres already one point by default

    # assign the point coordinates to the spline points
    for p, new_co in zip(spline.points, coords_list):
        new_co = randomize_xyz(new_co, s_x, s_y, s_z)
        p.co = (new_co + [1.0]) # (add nurbs weight)
        
    # make a new object with the curve

    obj = bpy.data.objects.new('gcode', crv)
    bpy.context.scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = bpy.data.objects['gcode']
    ###########
    
def add_spline_from_gcode_bezier(filename):
    coords_list = np.load(filename)       
    coords_list = np.array(coords_list[::10,1:] / 10).tolist()
    coords_list = center_obj(coords_list)
    print(coords_list)
    #coords_list = [[0,1,2], [1,2,3], [-3,2,1], [0,0,-4]]

    # make a new curve
    crv = bpy.data.curves.new('crv', 'CURVE')
    crv.dimensions = '3D'

    # make a new spline in that curve
    spline = crv.splines.new(type='BEZIER')

    # a spline point for each point
    spline.bezier_points.add(len(coords_list)-1) # theres already one point by default

    # assign the point coordinates to the spline points
    i = 0
    for p, new_co in zip(spline.bezier_points, coords_list):
        p.co = (new_co ) # (add nurbs weight)
        p.handle_left = spline.bezier_points[max(i-1,0)].co
        p.handle_right = spline.bezier_points[min(i+1,len(coords_list)-1)].co
        i += 1

    # make a new object with the curve

    obj = bpy.data.objects.new('gcode', crv)
    bpy.context.scene.collection.objects.link(obj)
    ###########
    
def create_random_sp(number_cuts, resize=[2,1,3], seed=0):
    ops.curve.primitive_bezier_circle_add(radius=1.0,
                                          location=(0.0, 0.0, 0.0),
                                          enter_editmode=True)

    # Subdivide the curve by a number of cuts, giving the
    # random vertex function more points to work with.
    ops.curve.subdivide(number_cuts=number_cuts)

    # Randomize the vertices of the bezier circle.
    # offset [-inf .. inf], uniform [0.0 .. 1.0],
    # normal [0.0 .. 1.0], RNG seed [0 .. 10000].
    ops.transform.vertex_random(offset=1.0, uniform=0.5, normal=0.0, seed=seed)

    # Scale the curve while in edit mode.
    ops.transform.resize(value=resize)
    bpy.context.object.name = "gcode"  

def edit_curve_appearence(bevel_depth=0.03, diffuse_color=[0.8,0.2,0.2,1.0]):
    ########
    # Return to object mode.
    ops.object.mode_set(mode='OBJECT')

    # Store a shortcut to the curve object's data.
    #obj_data = bpy.data.objects['gcode.001'].data
    obj_data = context.active_object.data

    # Which parts of the curve to extrude ['HALF', 'FRONT', 'BACK', 'FULL'].
    obj_data.fill_mode = 'FULL'

    # Breadth of extrusion
    #obj_data.extrude = 0.125

    # Depth of extrusion.
    obj_data.bevel_depth = bevel_depth

    # Smoothness of the segments on the curve.
    obj_data.resolution_u = 20
    obj_data.render_resolution_u = 32

    # Return to object mode.
    ops.object.mode_set(mode='OBJECT')

    # Convert from a curve to a mesh.
    print(bpy.context.object.type)
    #ops.object.convert(target='MESH')
    print(bpy.context.object.type)
    # Create a material
    mat = bpy.data.materials.new("color")

    ops.object.mode_set(mode='OBJECT')

    mat.diffuse_color = diffuse_color

    obj_data = context.active_object.data
    obj_data.materials.append(mat)
    ops.object.mode_set(mode='OBJECT')

def add_lights(num_lights, light_energy=30, range_l=[3,7]):
    #Inserts lights
    #Set number of lights; set to 3 for debug, but line directly below can be removed
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    #Finds the amount of lights that are going to be used
    lights = random.randint(1, num_lights)
    #Makes new lights the randomized amount of time
    for num in range(0, num_lights):
        light_data = bpy.data.lights.new(name="light_"+str(num), type='POINT')
        light_data.energy = light_energy
        light_object = bpy.data.objects.new(name="light_"+str(num), object_data=light_data)
        bpy.context.collection.objects.link(light_object)
        bpy.context.view_layer.objects.active = light_object
        light_object.location = (rand_in_range2(range_l), rand_in_range2(range_l), rand_in_range2(range_l))
        dg = bpy.context.evaluated_depsgraph_get() 
        dg.update()

def delete_all_obj():
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.select_by_type(type='CURVE')
    bpy.ops.object.delete()

def rand_in_range2(range):
    sign = [-1,1][random.randrange(2)]
    res = sign * random.uniform(range[0],range[1])
    return res

def save_render(path_out, num_rotation_steps=2):
    #set your own target here
    target = bpy.data.objects['gcode']
    cam = bpy.data.objects['Camera']
    t_loc_x = target.location.x
    t_loc_y = target.location.y
    cam_loc_x = cam.location.x
    cam_loc_y = cam.location.y

    #dist = sqrt((t_loc_x-cam_loc_x)**2+(t_loc_y-cam_loc_y)**2)
    dist = (target.location.xy-cam.location.xy).length
    #ugly fix to get the initial angle right
    init_angle  = (1-2*bool((cam_loc_y-t_loc_y)<0))*acos((cam_loc_x-t_loc_x)/dist)-2*pi*bool((cam_loc_y-t_loc_y)<0)
    for x in range(num_rotation_steps):
        alpha = init_angle + (x+1)*2*pi/num_rotation_steps
        cam.rotation_euler[2] = pi/2+alpha
        cam.location.x = t_loc_x+cos(alpha)*dist
        cam.location.y = t_loc_y+sin(alpha)*dist
        file = os.path.join(path_out, str(x))
        bpy.context.scene.render.filepath = file
        bpy.ops.render.render( write_still=True )

from mathutils import Vector
from glob import glob
import math
def save_render2(path_out, num_rotation_steps=2, h_range=[30, 80], bckg_transparent=True):
    camera = bpy.data.objects['Camera']  # Make sure your first camera is named 'MainCamera'
    print(camera.type)
    # set radius vector in polar coords
    r = Vector((camera.location[0], camera.location[1], camera.location[2])).length
    # set target
    target = bpy.data.objects['gcode']
    t_loc_x = target.location.x
    t_loc_y = target.location.y
    bpy.context.view_layer.objects.active = target
    bpy.context.active_object.select_set(state=True)

    # Add a new track to constraint and set it to track your object
    bpy.context.view_layer.objects.active = camera
    track_to = bpy.context.object.constraints.new('TRACK_TO')
    track_to.target = target
    track_to.track_axis = 'TRACK_NEGATIVE_Z'
    track_to.up_axis = 'UP_Y'

    files_num = len(glob(os.path.join(path_out, "*")))
    for step_num in range(files_num, files_num+num_rotation_steps):
        h = math.radians(random.uniform(h_range[0],h_range[1]))
        alpha = 2 * math.pi * random.random()
        x = r * math.cos(h) * math.cos(alpha)
        y = r * math.cos(h) * math.sin(alpha)
        z = r * math.sin(h)

        x += t_loc_x
        y += t_loc_y

        camera.location.x = x
        camera.location.y = y
        camera.location.z = z
        # save render
        file = os.path.join(path_out, str(step_num))
        if bckg_transparent:
            bpy.context.scene.render.film_transparent = True
        else:
            bpy.context.scene.render.film_transparent = False
        bpy.context.scene.render.image_settings.color_mode = 'RGBA'
        # bpy.ops.view3d.camera_to_view_selected()
        bpy.context.scene.render.filepath = file
        bpy.context.scene.render.resolution_x = 2000 #3840 #1920
        bpy.context.scene.render.resolution_y = 2000 #3840 #1080
        bpy.ops.render.render( write_still=True )
