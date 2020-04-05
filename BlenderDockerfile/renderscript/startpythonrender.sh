#!/bin/bash

/usr/local/blender/blender -b /home/shared/$QUEUE.blend --python /home/script/pythonRender.py
status=$?
while [ $status -gt 0 ]
do
/usr/local/blender/blender -b /home/shared/$QUEUE.blend --python /home/script/pythonRender.py
status=$?
done

while [ 900000  -gt $status ]
do 
/usr/local/blender/blender -b /home/shared/$QUEUE.blend --python /home/script/pythonRender.py
status=$?
done
exit $status