#!/bin/bash
incomingname=$1
#some logging for testing
echo $incomingname > /home/enqueueStdout 

KUBE_TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
echo $KUBE_TOKEN >> /home/enqueueStdout

#some analysis
regex="([\.a-zA-Z0-9\-]+).blend"
if [[ ${incomingname} =~ $regex ]]
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

# /usr/local/blender/blender -b -noaudio /home/shared/$incomingname --python /home/nodejs/analyzer.sh '"/home/shared/"$incomingname'
# FrameEstimateSec=$(</home/shared/$(podname)/somefile)
# FPS=1
# x = (FrameEstimateSec / vCPUanalyser) / (1/FPS) 
# x = number of vcpus

# REM Read from file, produced by analyser script

numberOfPodsRequired=1

#resourceRequirements=$(</home/shared/$(podname)/somefile)


image=$TASKMANAGERIMAGE



$(printf "%s" "{\"apiVersion\": \"v1\",\"kind\": \"Pod\",\"metadata\": { \"name\": \""$podname"\"},\"spec\": { \"containers\": [ {\"name\": \""$podname"\",\"image\": \""$image"\", \"resources\": { \"limits\":{\"cpu\": \"100m\"},\"requests\":{\"cpu\": \"50m\"}}, \"env\":  [{\"name\": \"BROKER_URL\",\"value\": \"amqp://guest:guest@rabbitmq-service:5672\"},{\"name\": \"QUEUE\",\"value\": \"tasklist\"},{\"name\": \"MY_POD_NAME\",\"valueFrom\":{\"fieldRef\":{\"fieldPath\": \"metadata.name\"}}}],\"volumeMounts\": [{\"mountPath\": \"/home/shared\",\"name\": \"volume\"}], \"ports\": [{\"containerPort\": 80}] }],\"volumes\":[{\"name\": \"volume\",\"persistentVolumeClaim\":{\"claimName\": \"shared-volume\"}}],\"serviceAccount\": \"pod-creation-sa\",\"serviceAccountName\": \"pod-creation-sa\"}}" > scriptprintf)

$(curl -k POST -H "Authorization: Bearer $KUBE_TOKEN" -H "Content-Type: application/json" https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_PORT_443_TCP_PORT/api/v1/namespaces/default/pods -d@scriptprintf >>/home/enqueueStdout)

image=$ENCODERIMAGE
resolution="1920x1080"
framerate="24"
startframe="0"

$(printf "%s" "{\"apiVersion\": \"v1\",\"kind\": \"Pod\",\"metadata\": { \"name\": \"encoder-"$podname"\"},\"spec\": { \"containers\": [ {\"name\": \"encoder-"$podname"\",\"image\": \""$image"\", \"resources\": { \"limits\":{\"cpu\": \"100m\"},\"requests\":{\"cpu\": \"50m\"}}, \"env\":  [{\"name\": \"BROKER_URL\",\"value\": \"amqp://guest:guest@rabbitmq-service:5672\"}, {\"name\": \"FOLDERNAME\",\"value\": \""$podname"\"},{\"name\": \"RESOLUTION\",\"value\": \""$resolution"\"},{\"name\": \"FRAMERATE\",\"value\": \""$framerate"\"},{\"name\": \"STARTFRAME\",\"value\": \""$startframe"\"},{\"name\": \"MY_POD_NAME\",\"valueFrom\":{\"fieldRef\":{\"fieldPath\": \"metadata.name\"}}}],\"volumeMounts\": [{\"mountPath\": \"/home/shared\",\"name\": \"volume\"}], \"ports\": [{\"containerPort\": 80}] }],\"volumes\":[{\"name\": \"volume\",\"persistentVolumeClaim\":{\"claimName\": \"shared-volume\"}}],\"serviceAccount\": \"pod-creation-sa\",\"serviceAccountName\": \"pod-creation-sa\"}}" > scriptprintf)

#{\"name\": \"FOLDERNAME\",\"value\": \""$podname"\"},
#{\"name\": \"RESOLUTION\",\"value\": \""$resolution"\"},
#{\"name\": \"FRAMERATE\",\"value\": \""$framerate"\"},
#{\"name\": \"STARTFRAME\",\"value\": \""$startframe"\"},
#{\"name\": \"MY_POD_NAME\",\"valueFrom\":{\"fieldRef\":{\"fieldPath\": \"metadata.name\"}}}


$(curl -k POST -H "Authorization: Bearer $KUBE_TOKEN" -H "Content-Type: application/json" https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_PORT_443_TCP_PORT/api/v1/namespaces/default/pods -d@scriptprintf >>/home/enqueueStdout)


echo ${podname} >>/home/enqueueStdout
echo ${numberOfPodsRequired} >>/home/enqueueStdout
echo ${resourceRequirements} >>/home/enqueueStdout



# enqueue task to tasklist
$(python3 ./nodejs/enqueueTaskToTaskQueue.py $podname $numberOfPodsRequired $resourceRequirements >> /home/enqueueStdout)

#entrypoint for taskmanager is adding the frames to frameQueue
#$(curl -k -X POST -d @- -H "Authorization: Bearer $KUBE_TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_PORT_443_TCP_PORT/api/v1/pods <<'EOF'{  "kind": "Pod",  "apiVersion": "v1",  ...}EOF)