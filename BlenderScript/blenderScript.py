# import sys
# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, 'C:/Users/Kim/Desktop/blender-2.80rc1-windows64/2.80/scripts/modules/')

import bpy
import blend_render_info


filepath = 'C:/Users/Kim/Desktop/Blender Projects/test_animation.blend'
data = blend_render_info.read_blend_rend_chunk(filepath)


###Base variables
start_frame = data[0][0]
end_frame = data[0][1]
scene_name = data[0][2]
total_frames = end_frame - start_frame
frame_list = []


##########################################################################################




###Get Frames
p10_frame = total_frames/100*10 #the 10% frame

# Select frame every 10% of total frames, finds 10 frames in total
for x in range(0, 10):
    frame_list.append(0 + (x * p10_frame) + start_frame)
##########################################################################################


###Get Tiles



total_tiles = ((bpy.context.scene.render.resolution_x.real * bpy.context.scene.render.resolution_y.real) / 
                (bpy.context.scene.render.tile_x.real * bpy.context.scene.render.tile_x.real))


p10_tiles = total_tiles/100*10

print(total_tiles)



# for x in range(0, p10_tiles):
    
    
# render settings
scene = bpy.context.scene
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = "C:/Users/Kim/Desktop/Blender Outputs/image.png"



#bpy.ops.view3d.render_border(xmin=1000, ymin=800, xmax=1920, ymax=1080)


# MinValueX = tileNr * TileSize / ResolutionX
# MinValueY = tileNr * TileSize / ResolutionY
# MaxValueX = (tileNr + 1) * TileSize / ResolutionX
# MaxValueY = (tileNr + 1) * TileSize / ResolutionY


minx = (7.5*64)/1920
miny = (4.21875*64)/1080


maxx = (7.5*64)*2/1920
maxy = (4.21875*64)*2/1080


bpy.context.scene.render.border_min_x = minx
bpy.context.scene.render.border_min_y = miny
bpy.context.scene.render.border_max_x = maxx
bpy.context.scene.render.border_max_y = maxy


bpy.context.scene.render.use_border = True
bpy.ops.render.render(write_still = 1)



##########################################################################################










# print("Total Frames for scene with name", scene_name, ":", total_frames )



# python "C:\Users\Kim\Desktop\blendeScript\blenderScript.py"