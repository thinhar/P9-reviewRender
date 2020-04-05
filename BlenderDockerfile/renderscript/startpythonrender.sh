#!/bin/bash

/usr/local/blender/blender -b /home/shared/$QUEUE.blend --python /home/script/pythonRender.py
status=$?
while [ $status -gt 0 ]
do
/usr/local/blender/blender -b /home/shared/$QUEUE.blend --python /home/script/pythonRender.py
status=$?
done

while [$status -gt -10000]
do 
/usr/local/blender/blender -b /home/shared/$QUEUE.blend --python /home/script/pythonRender.py
status=$?
done
exit $status