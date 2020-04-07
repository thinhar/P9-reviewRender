#!/bin/bash
task_id=$1
#some logging for testing
echo $task_id > /home/enqueueStdout 

KUBE_TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
echo $KUBE_TOKEN >> /home/enqueueStdout

#some analysis
regex="([\.a-zA-Z0-9\-]+).blend"
if [[ ${task_id} =~ $regex ]]
then
    podname="${BASH_REMATCH[1]}"
	#echo ${podname}

fi

############################ shitty analysis change duo task
if [ ! -f /home/somefile ]; then
     printf "%s" "C1000"> /home/somefile
fi

resourceRequirements=$(</home/somefile)
if [[ ${resourceRequirements} == "C1000" ]]
then
        printf "%s" "C500"> /home/somefile
else
        printf "%s" "C1000"> /home/somefile
fi
############################## shitty analysis change duo task

# /usr/local/blender/blender -b -noaudio /home/shared/$task_id --python /home/nodejs/analyzer.sh '"/home/shared/"$task_id'
# FrameEstimateSec=$(</home/shared/$(podname)/somefile)
# FPS=1
# x = (FrameEstimateSec / vCPUanalyser) / (1/FPS) 
# x = number of vcpus

# REM Read from file, produced by analyser script

render_workers_required=1

#resourceRequirements=$(</home/shared/$(podname)/somefile)


image=$TASKMANAGERIMAGE


/usr/local/blender/blender -b /home/shared/$task_id --python /home/BlenderScript/blenderScript.py -- ${task_id} >>/home/enqueueStdout

IFS=';' read -ra ADDR <<< $(</home/shared/${task_id}/output.txt)

frame_resolution_x = ADDR[0] 
frame_resolution_y = ADDR[1]
resolution = "${frame_resolution_x}x${frame_resolution_y}"
startframe = ADDR[2]
frames_in_scene = ADDR[3]
framerate = ADDR[4]
aprox_frame_render_time = ADDR[5]


### Functions
ScaleClusterHorizontal()
{
    #Fancy Scaling gl, poopguy
}




# Math Section
### x = (FrameEstimateSec / vCPUanalyser) / (1/FPS) 
requested_framerate = 0.02

required_vCPU = (aprox_frame_render_time / 0.1) / (1 / requested_framerate) 
available_vCPU_on_node[] = kubectl describe nodes | grep -A 2 -e "^\s*CPU Requests"
SUM_available_vCPU=$(IFS=+; echo "$((${available_vCPU_on_node[*]}))")

render_workers_vCPU = 1 # UNSURE: do we need to declare it, before use?

# Check if cluster requires scaling
if [ required_vCPU > SUM_available_vCPU ]
then
    cluster_missing_vCPU = required_vCPU - SUM_available_vCPU
    ScaleClusterHorizontal cluster_missing_vCPU
fi


# Check case to determine $render_workers_required
if [ requested_framerate < 1 ]
then
    render_workers_required = 1 # requested_framerate * (1/requested_framerate)
    render_workers_vCPU = required_vCPU
else
   render_workers_required = math.Round(requested_framerate)
   render_workers_vCPU = vCPU / render_workers_required
fi




AddRenderWorkersToQueue render_workers_required

AddRenderWorkersToQueue()
{
    available_render_worker_hosts_spots = 0

    for i in nodes
    do
        NUMBER = Node_List[i].available_vCPU_on_a_single_node / render_workers_vCPU
        x = python -c "from math import floor; print floor($NUMBER)"
        x = x + available_render_worker_hosts_spots

        #available_render_worker_hosts_spots += (int)math.Floor(Node_List[i].available_vCPU_on_a_single_node / render_workers_vCPU)
    done


    if [required_vCPU > Node_vCPU_Capacity] || [ $1 > available_render_worker_hosts_spots ]
    then
        if [ $1 > frames_in_scene ] || [ $1 > 99999 ]  #TODO: use mem_peak or mem_avg to calulate max number of worker pods
        then
            sa
        else
            # Make sub-tasks with sub-frames ( render_workers_required * 2)
            # TODO: Add sub-frames logic here
            AddRenderWorkersToQueue ($1 * 2)
        fi
    else
        # enqueue task to tasklist
        resourceRequirements = required_vCPU / $1
        $(python3 ./nodejs/enqueueTaskToTaskQueue.py $podname $1 $resourceRequirements >> /home/enqueueStdout)
    fi
}





$(printf "%s" "{\"apiVersion\": \"v1\",\"kind\": \"Pod\",\"metadata\": { \"name\": \""$podname"\"},\"spec\": { \"containers\": [ {\"name\": \""$podname"\",\"image\": \""$image"\", \"resources\": { \"limits\":{\"cpu\": \"100m\"},\"requests\":{\"cpu\": \"50m\"}}, \"env\":  [{\"name\": \"BROKER_URL\",\"value\": \"amqp://guest:guest@rabbitmq-service:5672\"}, {\"name\": \"STARTFRAME\",\"value\": \""$startframe"\"}, {\"name\": \"FRAMES_IN_SCENE\",\"value\": \""$frames_in_scene"\"}, {\"name\": \"QUEUE\",\"value\": \"tasklist\"},{\"name\": \"MY_POD_NAME\",\"valueFrom\":{\"fieldRef\":{\"fieldPath\": \"metadata.name\"}}}],\"volumeMounts\": [{\"mountPath\": \"/home/shared\",\"name\": \"volume\"}], \"ports\": [{\"containerPort\": 80}] }],\"volumes\":[{\"name\": \"volume\",\"persistentVolumeClaim\":{\"claimName\": \"shared-volume\"}}],\"serviceAccount\": \"pod-creation-sa\",\"serviceAccountName\": \"pod-creation-sa\"}}" > scriptprintf)

$(curl -k POST -H "Authorization: Bearer $KUBE_TOKEN" -H "Content-Type: application/json" https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_PORT_443_TCP_PORT/api/v1/namespaces/default/pods -d@scriptprintf >>/home/enqueueStdout)

image=$ENCODERIMAGE

$(printf "%s" "{\"apiVersion\": \"v1\",\"kind\": \"Pod\",\"metadata\": { \"name\": \"encoder-"$podname"\"},\"spec\": { \"containers\": [ {\"name\": \"encoder-"$podname"\",\"image\": \""$image"\", \"resources\": { \"limits\":{\"cpu\": \"100m\"},\"requests\":{\"cpu\": \"50m\"}}, \"env\":  [{\"name\": \"BROKER_URL\",\"value\": \"amqp://guest:guest@rabbitmq-service:5672\"}, {\"name\": \"FOLDERNAME\",\"value\": \""$podname"\"},{\"name\": \"RESOLUTION\",\"value\": \""$resolution"\"},{\"name\": \"FRAMERATE\",\"value\": \""$framerate"\"},{\"name\": \"STARTFRAME\",\"value\": \""$startframe"\"},{\"name\": \"MY_POD_NAME\",\"valueFrom\":{\"fieldRef\":{\"fieldPath\": \"metadata.name\"}}}],\"volumeMounts\": [{\"mountPath\": \"/home/shared\",\"name\": \"volume\"}], \"ports\": [{\"containerPort\": 80}] }],\"volumes\":[{\"name\": \"volume\",\"persistentVolumeClaim\":{\"claimName\": \"shared-volume\"}}],\"serviceAccount\": \"pod-creation-sa\",\"serviceAccountName\": \"pod-creation-sa\"}}" > scriptprintf)

#{\"name\": \"FOLDERNAME\",\"value\": \""$podname"\"},
#{\"name\": \"RESOLUTION\",\"value\": \""$resolution"\"},
#{\"name\": \"FRAMERATE\",\"value\": \""$framerate"\"},
#{\"name\": \"STARTFRAME\",\"value\": \""$startframe"\"},
#{\"name\": \"MY_POD_NAME\",\"valueFrom\":{\"fieldRef\":{\"fieldPath\": \"metadata.name\"}}}


$(curl -k POST -H "Authorization: Bearer $KUBE_TOKEN" -H "Content-Type: application/json" https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_PORT_443_TCP_PORT/api/v1/namespaces/default/pods -d@scriptprintf >>/home/enqueueStdout)


echo ${podname} >>/home/enqueueStdout
echo ${render_workers_required} >>/home/enqueueStdout
echo ${resourceRequirements} >>/home/enqueueStdout



# enqueue task to tasklist
#$(python3 ./nodejs/enqueueTaskToTaskQueue.py $podname $render_workers_required $resourceRequirements >> /home/enqueueStdout)

#entrypoint for taskmanager is adding the frames to frameQueue
#$(curl -k -X POST -d @- -H "Authorization: Bearer $KUBE_TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_PORT_443_TCP_PORT/api/v1/pods <<'EOF'{  "kind": "Pod",  "apiVersion": "v1",  ...}EOF)