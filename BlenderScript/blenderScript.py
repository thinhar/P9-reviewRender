# import sys
# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, 'C:/Users/Kim/Desktop/blender-2.80rc1-windows64/2.80/scripts/modules/')

import bpy
import blend_render_info
import math


#import time
#import multiprocessing as mp


from datetime import datetime
from bpy.app import handlers
import time
#time.clock()

from decimal import Decimal


FRAME_START_TIME = None
FRAME_START_TIME2 = Decimal(0.0)
FRAME_END_TIME = Decimal(0.0)

RENDER_START_TIME = None

TOTAL_TIME = Decimal(0.0)



def handler_function(name):
    def handler(scene):
        print(name)
    return handler

frame_handlers = [getattr(handlers, name)
        for name in dir(handlers) if name.startswith("render_")]

#def add_dummy_handlers():
#    for  handler in frame_handlers:
#        handler.append(handler_function(name))   

def clear_handlers():
    for  handler in frame_handlers:
        handler.clear()

def render_init(scene):
    global RENDER_START_TIME
    global RENDER_START_TIME2
    RENDER_START_TIME = datetime.now()  
    RENDER_START_TIME2 = Decimal(time.time())    
    print("Render Start")  

#def render_pre(scene):
#    global FRAME_START_TIME
#    FRAME_START_TIME = datetime.now()

#def render_stats(dummy):
#    print("Elapsed:", datetime.now() - FRAME_START_TIME)

def complete(scene):
    print("Total:",  datetime.now() - RENDER_START_TIME)
    
    global TOTAL_TIME 
    global FRAME_END_TIME 
    FRAME_END_TIME = Decimal(time.time())
    
    
    print("START: ", RENDER_START_TIME2)
    print("END: ", FRAME_END_TIME)
    

    #global FRAME_END_TIME
    #global FRAME_START_TIME2
    temp = FRAME_END_TIME - RENDER_START_TIME2
    print("FINAL: ", temp)   
    
    
    
    #elapsed_time = FRAME_END_TIME - FRAME_START_TIME2
    
    #print("FINAL: ", elapsed_time)
    
    
    #global FRAME_START_TIME 
    #FRAME_END_TIME = time.time()
   
    #te = time.time()  
    #elapsed_time = time.time() - FRAME_START_TIME
    #TOTAL_TIME = time.time() - FRAME_START_TIME2

    #print(te - FRAME_START_TIME)
    
    #TOTAL_TIME += (datetime.now() - RENDER_START_TIME)
    
    
    
    
    #frame_list[0].append((datetime.now() - RENDER_START_TIME))


def cancel(scene):
    print("CANCELLED.... After:",  datetime.now() - FRAME_START_TIME)

clear_handlers()

handlers.render_init.append(render_init)
#handlers.render_pre.append(render_pre)
#handlers.render_stats.append(render_stats) # write or post ?
handlers.render_complete.append(complete)
handlers.render_cancel.append(cancel)













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
 
 
#print(total_x_tiles_in_a_row)
#print(total_y_tiles_in_a_row)
 
print("P10:", p10_tiles_in_frame)  
 
print("beee", total_tiles_in_frame)
 
 
 
 
#while i < total_x_tiles_in_frame / tile_interval_x:
#    if i == 0:
#        minx = tile_size / scene.render.resolution_x.real
#        maxx = 2 * tile_size / scene.render.resolution_x.real
#    else:    
#        minx = (i * tile_interval_x * tile_size) / scene.render.resolution_x.real
#        maxx = ((i + 1) * tile_interval_x * tile_size) / scene.render.resolution_x.real
#
#
#
#    while l < total_y_tiles_in_frame / tile_interval_y:
#        if l == 0:
#            miny = tile_size / scene.render.resolution_y.real
#            maxy = 2 * tile_size / scene.render.resolution_y.real
#        else:  
#            miny = (l * tile_interval_y * tile_size) / scene.render.resolution_y.real
#            maxy = ((l + 1) * tile_interval_y * tile_size) / scene.render.resolution_y.real          
#        l += 1
#    i += 1


#def renderTile(minx, miny, maxx, maxy):
#    
#    global imageNumber
#    str_temp = str(imageNumber)
#    
#    # render settings
#    scene.render.image_settings.file_format = 'PNG'
#    scene.render.filepath = "C:/Users/Kim/Desktop/Blender Outputs/" + str_temp + "image.PNG"

#    bpy.context.scene.render.border_min_x = minx
#    bpy.context.scene.render.border_min_y = miny
#    bpy.context.scene.render.border_max_x = maxx
#    bpy.context.scene.render.border_max_y = maxy


#    bpy.context.scene.render.use_border = True
#    bpy.ops.render.render(write_still = 1)
#    
#    imageNumber += 1
#    return







imageNumber = 0


def renderTile(minx, miny, maxx, maxy):
    
    global imageNumber
    str_temp = str(imageNumber)
    
    # render settings
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = "C:/Users/Kim/Desktop/Blender Outputs/" + str_temp + "image.PNG"

    bpy.context.scene.render.border_min_x = minx
    bpy.context.scene.render.border_min_y = miny
    bpy.context.scene.render.border_max_x = maxx
    bpy.context.scene.render.border_max_y = maxy


    # Global Render Settings
    bpy.context.scene.cycles.samples = 1
    bpy.context.scene.render.use_border = True
    bpy.ops.render.render(write_still = 1)
    
    
    
    imageNumber += 1

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
                #renderTile(minx, miny, maxx, maxy)
                #print(minx, miny, maxx, maxy)        
                #pool.apply_async(renderTile, (minx, miny, maxx, maxy))
                tiles_rendered += 1   
                l += 1
        i += 1
        l = 1

    #pool.close()


findTileRenderRegions()



#renderTile(0, 0, 1, 1)
#renderTile(0, 0, 0.01, 0.01)

#print("t1")
#renderTile(0, 0, 0.01, 0.01)
#print("t2")
#renderTile(0, 0, 0.001, 0.001)




#print("t4")
#renderTile(0, 0, 0.0009301, 0.0009301)
#print("t4")
#renderTile(0, 0, 1, 1)







renderTile(0.38830368802245047, 0.3155292041681043, 0.4216370213557838, 0.37478846342736355)







#while i <= math.ceil(total_x_tiles_in_frame / tile_interval_x):  
#    minx = (i * tile_interval_x * scene.render.tile_x.real) / scene.render.resolution_x.real
#    maxx = (i * tile_interval_x * scene.render.tile_x.real + scene.render.tile_x.real) / scene.render.resolution_x.real


#    while l <= math.ceil(total_y_tiles_in_frame / tile_interval_y):
#        if tiles_rendered > p10_tiles_in_frame:
#            break

#        miny = (l * tile_interval_y * scene.render.tile_y.real) / scene.render.resolution_y.real
#        maxy = (l * tile_interval_y * scene.render.tile_y.real + scene.render.tile_y.real) / scene.render.resolution_y.real

#        renderTile(minx, miny, maxx, maxy)
#        tiles_rendered += 1        
#        l += 1
#    i += 1
#    l = 1
















    
    
    
    














