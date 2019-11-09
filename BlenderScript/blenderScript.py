# import sys
# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, 'C:/Users/Kim/Desktop/blender-2.80rc1-windows64/2.80/scripts/modules/')

import bpy
import blend_render_info
import math


#import time
#import multiprocessing as mp


from datetime import datetime
from bpy.app import handlers # https://docs.blender.org/api/current/bpy.app.handlers.html#bpy.app.handlers.render_post
import time

from decimal import Decimal







RENDER_START_TIME2 = 0.0
TOTAL_TIME_USED_ONE_SAMPLE2 = Decimal(0.0)


def render_pre(scene):
    global RENDER_START_TIME2
    RENDER_START_TIME2 = time.time()



def render_post(scene):
    elapsed_time = (time.time() - RENDER_START_TIME2) 
    print("TIME1: ", elapsed_time)   
    
    global TOTAL_TIME_USED_ONE_SAMPLE2
    TOTAL_TIME_USED_ONE_SAMPLE2 += Decimal(elapsed_time / bpy.context.scene.cycles.samples)






RENDER_START_TIME = 0.0
TOTAL_TIME_USED_ONE_SAMPLE = Decimal(0.0)


def handler_function(name):
    def handler(scene):
        print(name)
    return handler

frame_handlers = [getattr(handlers, name)
        for name in dir(handlers) if name.startswith("render_")]


def clear_handlers():
    for  handler in frame_handlers:
        handler.clear()

def render_init(scene):    
    global RENDER_START_TIME
    RENDER_START_TIME = time.time()   
    



def complete(scene):    
    elapsed_time = (time.time() - RENDER_START_TIME) 
    print("TIME2: ", elapsed_time)   
    
    #temp = Decimal((time.time() - RENDER_START_TIME) / bpy.context.scene.cycles.samples)
    #print("TIME: ", temp)   

    global TOTAL_TIME_USED_ONE_SAMPLE
    TOTAL_TIME_USED_ONE_SAMPLE += Decimal(elapsed_time / bpy.context.scene.cycles.samples)
    

    


clear_handlers()

handlers.render_init.append(render_init)
handlers.render_complete.append(complete)


handlers.render_pre.append(render_pre)
handlers.render_post.append(render_post)










filepath = 'C:/Users/Kim/Desktop/Blender Projects/test_animation.blend'
data = blend_render_info.read_blend_rend_chunk(filepath)


###Base variables
start_frame = data[0][0]
end_frame = data[0][1]
scene_name = data[0][2]
total_frames_in_scene = end_frame - start_frame
frame_list = []

scene = bpy.context.scene

##########################################################################################


###Get Frames
p10_frame_in_scene = total_frames_in_scene * 0.10 #the 10% frame

# Select frame every 10% of total frames, finds 10 frames in total
for x in range(0, 10):
    frame_list.append(0 + (x * p10_frame_in_scene) + start_frame) # todo: add ceil or floor?
##########################################################################################














###Get Tiles
total_x_tiles_in_frame = (scene.render.resolution_x.real - (2 * scene.render.tile_x.real)) / scene.render.tile_x.real
total_y_tiles_in_frame = (scene.render.resolution_y.real - (2 * scene.render.tile_y.real)) / scene.render.tile_y.real
total_tiles_in_frame = total_x_tiles_in_frame * total_y_tiles_in_frame
p10_tiles_in_frame = total_tiles_in_frame * 0.10



# Find tile interval for x and y axis
total_x_tiles_in_a_row = math.sqrt(p10_tiles_in_frame * total_x_tiles_in_frame / total_y_tiles_in_frame)

#total_y_tiles_in_a_row = (p10_tiles_in_frame / total_x_tiles_in_a_row) #test

tile_interval_x = total_x_tiles_in_frame / total_x_tiles_in_a_row
tile_interval_y = total_y_tiles_in_frame / (p10_tiles_in_frame / total_x_tiles_in_a_row)
 
 
 


IMAGE_NUMBER = 0

def renderTile(minx, miny, maxx, maxy, samples):
    global IMAGE_NUMBER
    str_temp = str(IMAGE_NUMBER)
    
    # render settings
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = "C:/Users/Kim/Desktop/Blender Outputs/" + str_temp + "image.PNG"

    bpy.context.scene.render.border_min_x = minx
    bpy.context.scene.render.border_min_y = miny
    bpy.context.scene.render.border_max_x = maxx
    bpy.context.scene.render.border_max_y = maxy

    # Global Render Settings
    bpy.context.scene.cycles.samples = samples
    bpy.context.scene.render.use_border = True
    bpy.ops.render.render(write_still = 0)
        
    IMAGE_NUMBER += 1

    return



def findTileRenderRegions(): 
    
    #pool = mp.Pool(mp.cpu_count())
    
    tiles_rendered = 1   
    
    miny = 0.0
    maxy = 0.0
  
    i = 1
    l = 1
    
    while i <= math.ceil(total_x_tiles_in_frame / tile_interval_x):  
        minx = ((i * tile_interval_x * scene.render.tile_x.real) - scene.render.tile_x.real) / scene.render.resolution_x.real
        maxx = (i * tile_interval_x * scene.render.tile_x.real) / scene.render.resolution_x.real

        if maxx > 1:
            break

        while l <= math.ceil(total_y_tiles_in_frame / tile_interval_y):
            if tiles_rendered > p10_tiles_in_frame:
                break

            miny = ((l * tile_interval_y * scene.render.tile_y.real) - scene.render.tile_y.real) / scene.render.resolution_y.real
            maxy = (l * tile_interval_y * scene.render.tile_y.real) / scene.render.resolution_y.real

            if maxy > 1:
                l = 1
                break
            else:
                print(IMAGE_NUMBER)
                renderTile(minx, miny, maxx, maxy, 1000)    
                #pool.apply_async(renderTile, (minx, miny, maxx, maxy))
                tiles_rendered += 1   
                l += 1
        i += 1
        l = 1

    #pool.close()


findTileRenderRegions()










user_render_task_samples = 512 # samples in the actual task from the user.


print("Estimated Frame Time1:", (( TOTAL_TIME_USED_ONE_SAMPLE2 / IMAGE_NUMBER ) * Decimal(total_tiles_in_frame) * user_render_task_samples))


print("Estimated Frame Time2:", (( TOTAL_TIME_USED_ONE_SAMPLE / IMAGE_NUMBER ) * Decimal(total_tiles_in_frame) * user_render_task_samples))




renderTile(0, 0, 1, 1, user_render_task_samples)













#print("t4")
#renderTile(0, 0, 0.0009301, 0.0009301)


#renderTile(0.38830368802245047, 0.3155292041681043, 0.4216370213557838, 0.37478846342736355)




















    
    
    
    














