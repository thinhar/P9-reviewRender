
import bpy
import blend_render_info
import math

from datetime import datetime
from bpy.app import handlers
import time

from decimal import Decimal




RENDER_START_TIME = 0.0
TOTAL_TIME_USED_ONE_SAMPLE = Decimal(0.0)
TOTAL_TIME_Analyse = Decimal(0.0)

def render_pre(scene):
    global RENDER_START_TIME
    RENDER_START_TIME = time.time()
    print("TIME: ", RENDER_START_TIME) 


def render_post(scene):
    elapsed_time = (time.time() - RENDER_START_TIME)
    print("Elapsed_TIME: ", elapsed_time)   
    
    global TOTAL_TIME_USED_ONE_SAMPLE
    TOTAL_TIME_USED_ONE_SAMPLE += Decimal(elapsed_time / bpy.context.scene.cycles.samples)

    global TOTAL_TIME_Analyse
    TOTAL_TIME_Analyse += Decimal(elapsed_time)


def handler_function(name):
    def handler(scene):
        print(name)
    return handler

frame_handlers = [getattr(handlers, name)
        for name in dir(handlers) if name.startswith("render_")]


def clear_handlers():
    for  handler in frame_handlers:
        handler.clear()


clear_handlers()

handlers.render_pre.append(render_pre)
handlers.render_post.append(render_post)




scene = bpy.context.scene

bpy.context.scene.render.tile_x = 64
bpy.context.scene.render.tile_y = 64


###Get Tiles
total_x_tiles_in_frame = (scene.render.resolution_x.real - (2 * scene.render.tile_x.real)) / scene.render.tile_x.real
total_y_tiles_in_frame = (scene.render.resolution_y.real - (2 * scene.render.tile_y.real)) / scene.render.tile_y.real
total_tiles_in_frame = total_x_tiles_in_frame * total_y_tiles_in_frame
p10_tiles_in_frame = total_tiles_in_frame * 0.04


# Find tile interval for x and y axis
total_x_tiles_in_a_row = math.sqrt(p10_tiles_in_frame * total_x_tiles_in_frame / total_y_tiles_in_frame)

tile_interval_x = total_x_tiles_in_frame / total_x_tiles_in_a_row
tile_interval_y = total_y_tiles_in_frame / (p10_tiles_in_frame / total_x_tiles_in_a_row)
 

IMAGE_NUMBER = 1

def renderTile(minx, miny, maxx, maxy, samples):
    
    global IMAGE_NUMBER

    # render settings
    scene.render.image_settings.file_format = 'PNG'

    bpy.context.scene.render.border_min_x = minx
    bpy.context.scene.render.border_min_y = miny
    bpy.context.scene.render.border_max_x = maxx
    bpy.context.scene.render.border_max_y = maxy

    # Global Render Settings
    bpy.context.scene.cycles.samples = samples
    bpy.context.scene.render.use_border = True
    bpy.context.scene.render.use_crop_to_border = True
    
    bpy.ops.render.render(write_still = 0)
        
    IMAGE_NUMBER += 1

    return



def findTileRenderRegions(samples):  
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
                renderTile(minx, miny, maxx, maxy, samples)    
                tiles_rendered += 1   
                l += 1
        i += 1
        l = 1


user_render_task_samples = bpy.context.scene.cycles.samples # samples in the actual task from the user.

findTileRenderRegions(50000)

print("Estimated Frame Time:", (( TOTAL_TIME_USED_ONE_SAMPLE / IMAGE_NUMBER ) * Decimal(total_tiles_in_frame) * user_render_task_samples ))

print("Total Analyse Time:", TOTAL_TIME_Analyse)


print("tileCount", IMAGE_NUMBER)














    
    
    
    














