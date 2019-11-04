# import sys
# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, 'C:/Users/Kim/Desktop/blender-2.80rc1-windows64/2.80/scripts/modules/')

import bpy
import blend_render_info
import math


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
    frame_list.append(0 + (x * p10_frame_in_scene) + start_frame)
##########################################################################################





###Get Tiles

#total_tiles = (
#               (bpy.context.scene.render.resolution_x.real * bpy.context.scene.render.resolution_y.real) / 
#               (bpy.context.scene.render.tile_x.real * bpy.context.scene.render.tile_x.real))


total_x_tiles_in_frame = (scene.render.resolution_x.real - (2 * scene.render.tile_x.real)) / scene.render.tile_x.real
total_y_tiles_in_frame = (scene.render.resolution_y.real - (2 * scene.render.tile_y.real)) / scene.render.tile_y.real
total_tiles_in_frame = total_x_tiles_in_frame * total_y_tiles_in_frame

p10_tiles_in_frame = total_tiles_in_frame * 0.10



# Find tile interval for x and y axis

total_x_tiles_in_a_row = math.sqrt(p10_tiles_in_frame * total_x_tiles_in_frame / total_y_tiles_in_frame)

total_y_tiles_in_a_row = (p10_tiles_in_frame / total_x_tiles_in_a_row) #test

tile_interval_x = total_x_tiles_in_frame / total_x_tiles_in_a_row
#tile_interval_y = total_y_tiles_in_frame / (total_x_tiles_in_frame / total_x_tiles_in_a_row)
tile_interval_y = total_y_tiles_in_frame / (p10_tiles_in_frame / total_x_tiles_in_a_row)
 
 
print(total_x_tiles_in_a_row)
print(total_y_tiles_in_a_row)
 
 
 

 
 
 
 
 
 
#print(tile_interval_x)    
#print(tile_interval_y)     
#print(p10_tiles_in_frame)     


#print("Total X tiles in frame:", total_x_tiles_in_frame)
#print("Total Y tiles in frame:", total_y_tiles_in_frame)

#print("Total tiles in frame:", total_tiles_in_frame)
#print("10 procent tiles in frame:", p10_tiles_in_frame)



#tile_size = 64

#minx = 0.0
#maxx = 0.0
#miny = 0.0
#maxy = 0.0

#i = 0
#l = 0
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


    bpy.context.scene.render.use_border = True
    bpy.ops.render.render(write_still = 1)
    
    imageNumber += 1
    return






tile_size_x = 60
tile_size_y = 108

minx = 0.0
maxx = 0.0
miny = 0.0
maxy = 0.0
#tileArray = [None] * math.ceil(p10_tiles_in_frame)

#i = 0
#l = 0

#while i < total_x_tiles_in_frame / tile_interval_x:
#    if i == 0:
#        minx = tile_size / scene.render.resolution_x.real
#        maxx = 2 * tile_size / scene.render.resolution_x.real            
#        #print("(", i, ")","Base MinX:", minx)
#        #print("(", i, ")","Base MaxX:", minx)
#    else:    
#        minx = (i * tile_interval_x * tile_size) / scene.render.resolution_x.real
#        maxx = ((i + 1) * tile_interval_x * tile_size) / scene.render.resolution_x.real
#        #print("(", i, ")","MinX:", minx)
#        #print("(", i, ")","MaxX:", minx)

#    while l < total_y_tiles_in_frame / tile_interval_y:
#        if l == 0:
#            miny = tile_size / scene.render.resolution_y.real
#            maxy = 2 * tile_size / scene.render.resolution_y.real
#            #print("(", l, ")","Base MinY:", miny)
#            #print("(", l, ")","Base MaxY:", maxy)
#        else:  
#            miny = (l * tile_interval_y * tile_size) / scene.render.resolution_y.real
#            maxy = ((l + 1) * tile_interval_y * tile_size) / scene.render.resolution_y.real
#            #print("(", l, ")","Base MinY:", miny)
#            #print("(", l, ")","Base MaxY:", maxy)
#        renderTile(minx, miny, maxx, maxy)        
#        l += 1
#    i += 1
#    l = 0















print(p10_tiles_in_frame)

#print(total_x_tiles_in_frame / tile_interval_x)
#print(total_y_tiles_in_frame / tile_interval_y)
#print(total_tiles_in_frame)

i = 1
l = 1
tiles_rendered = 1

while i <= math.ceil(total_x_tiles_in_frame / tile_interval_x):  
    minx = (i * tile_interval_x * scene.render.tile_x.real) / scene.render.resolution_x.real
    maxx = (i * tile_interval_x * scene.render.tile_x.real + scene.render.tile_x.real) / scene.render.resolution_x.real

    while l <= math.ceil(total_y_tiles_in_frame / tile_interval_y):
        if tiles_rendered > p10_tiles_in_frame:
            break
        
        miny = (l * tile_interval_y * scene.render.tile_y.real) / scene.render.resolution_y.real
        maxy = (l * tile_interval_y * scene.render.tile_y.real + scene.render.tile_y.real) / scene.render.resolution_y.real

        renderTile(minx, miny, maxx, maxy)
        tiles_rendered += 1        
        l += 1
    i += 1
    l = 1





























#for x in range(0, p10_tiles):
    
    
    
    
    




#bpy.ops.view3d.render_border(xmin=1000, ymin=800, xmax=1920, ymax=1080)

# MinValueX = tileNr * TileSize / ResolutionX
# MinValueY = tileNr * TileSize / ResolutionY
# MaxValueX = (tileNr + 1) * TileSize / ResolutionX
# MaxValueY = (tileNr + 1) * TileSize / ResolutionY










##########################################################################################










# print("Total Frames for scene with name", scene_name, ":", total_frames )



# python "C:\Users\Kim\Desktop\blendeScript\blenderScript.py"