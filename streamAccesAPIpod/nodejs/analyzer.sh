#!/bin/bash
incomingname=$1

#some analysis
echo $incomingname > /home/enqueueStdout 
KUBE_TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
echo $KUBE_TOKEN >> /home/enqueueStdout
numberOfPodsRequired=5
resourceRequirements="C1000"

#$(curl -k -X POST -d @- -H "Authorization: Bearer $KUBE_TOKEN"  -H 'Accept: application/json' -H 'Content-Type: application/json'  https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_PORT_443_TCP_PORT/api/v1/pods <<'EOF')

image="thinhar/taskmanager:0.08"
regex="([\.a-zA-Z0-9\-]+).blend"
if [[ ${incomingname} =~ $regex ]]
then
    podname="${BASH_REMATCH[1]}"
	echo ${podname}

fi

$(printf "%s" "{\"apiVersion\": \"v1\",\"kind\": \"Pod\",\"metadata\": { \"name\": \""$podname"\"},\"spec\": { \"containers\": [ {\"name\": \""$podname"\",\"image\": \""$image"\", \"resources\": { \"limits\":{\"cpu\": \"100m\"},\"requests\":{\"cpu\": \"50m\"}}, \"env\":  [{\"name\": \"BROKER_URL\",\"value\": \"amqp://guest:guest@rabbitmq-service:5672\"},{\"name\": \"QUEUE\",\"value\": \"tasklist\"},{\"name\": \"MY_POD_NAME\",\"valueFrom\":{\"fieldRef\":{\"fieldPath\": \"metadata.name\"}}}],\"volumeMounts\": [{\"mountPath\": \"/home/shared\",\"name\": \"volume\"}], \"ports\": [{\"containerPort\": 80}] }],\"volumes\":[{\"name\": \"volume\",\"persistentVolumeClaim\":{\"claimName\": \"shared-volume\"}}],\"serviceAccount\": \"pod-creation-sa\",\"serviceAccountName\": \"pod-creation-sa\"}}" > scriptprintf)

$(curl -k POST -H "Authorization: Bearer $KUBE_TOKEN" -H "Content-Type: application/json" https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_PORT_443_TCP_PORT/api/v1/namespaces/default/pods -d@scriptprintf >>/home/enqueueStdout)

echo ${podname} >>/home/enqueueStdout
echo ${numberOfPodsRequired} >>/home/enqueueStdout
echo ${resourceRequirements} >>/home/enqueueStdout



# enqueue task to tasklist
$(python3 ./nodejs/enqueueTaskToTaskQueue.py $podname $numberOfPodsRequired $resourceRequirements >> /home/enqueueStdout)

#entrypoint for taskmanager is adding the frames to frameQueue
#$(curl -k -X POST -d @- -H "Authorization: Bearer $KUBE_TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_PORT_443_TCP_PORT/api/v1/pods <<'EOF'{  "kind": "Pod",  "apiVersion": "v1",  ...}EOF)