#!/bin/bash

/usr/local/blender/blender -b -noaudio /home/shared/$QUEUE.blend --python /home/script/pythonRender.py
status=$?
while [ $status -gt 0 ]
do
/usr/local/blender/blender -b -noaudio /home/shared/$QUEUE.blend --python /home/script/pythonRender.py
status=$?
done
read -p " get user input" name
exit $status