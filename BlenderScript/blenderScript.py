import os
import bpy

#Base Settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.render.threads_mode = 'AUTO'
scene.cycles.tile_order = 'DISTRIBUTED_SELECTION'
scene.render.tile_x = 64
scene.render.tile_y = 64
scene.frame_step = 10
user_render_task_samples = scene.cycles.samples # samples in the actual task from the user.
scene.cycles.short_circuit_time = 1
scene.cycles.analyser_percentage = 0.03
scene.cycles.samples = 1000000

#Output Settings
scene.render.image_settings.file_format = 'JPEG'
scene.render.image_settings.color_mode = 'RGB'
scene.render.image_settings.quality = 90
scene.render.use_overwrite = True
scene.render.filepath = '//frame_#####'

# Start Rendering
bpy.ops.render.render(animation = True)


sample_count_sum = 0
render_time_sum = 0.0

with open("sample_output.txt","r") as f:
    for item in map(lambda x: x.split(","), f.read().split(";")):
        if item[0]:
            sample_count_sum += int(item[0])
            render_time_sum += float(item[1])

os.remove("sample_output.txt")

averageTilecount=sample_count_sum/render_time_sum

total_x_tiles_in_frame = scene.render.resolution_x.real / scene.render.tile_x.real
total_y_tiles_in_frame = scene.render.resolution_y.real / scene.render.tile_y.real
total_tiles_in_frame = total_x_tiles_in_frame * total_y_tiles_in_frame

total_samples = (user_render_task_samples*total_tiles_in_frame)
samples_pr_sec = averageTilecount * scene.render.threads

# Output variables for the Task Manager
aprox_frame_render_time = total_samples/samples_pr_sec
frame_resolution_x = scene.render.tile_x.real
frame_resolution_y = scene.render.tile_y.real
start_frame = scene.frame_start
frames_in_scene = scene.frame_end - scene.frame_start
animation_framerate = scene.render.fps


str_output = str(frame_resolution_x) + ";" + str(frame_resolution_y) + ";" + str(start_frame) + ";" + str(frames_in_scene) + ";" + str(animation_framerate) + ";" + str(aprox_frame_render_time)

f = open(bpy.path.abspath("//output.txt"), "w")
f.write(str_output)
f.close()

#print(frame_resolution_x, ";", frame_resolution_y, ";", start_frame, ";", frames_in_scene, ";", animation_framerate, ";", aprox_frame_render_time)


   