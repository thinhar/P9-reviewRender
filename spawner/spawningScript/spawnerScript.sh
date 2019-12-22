#!/bin/bash
# test stuff
echo "start spawnscript"
KUBE_TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
i=1
while true
do
	taskqueueresult=$(/usr/bin/amqp-consume --url=$BROKER_URL -q $QUEUE -c 1 cat && echo)
	
	echo "${taskqueueresult}"
	#|grep -P '(?:[a-zA-z1-9-]+ C)([\d]+)' -o

	regex="([\.a-zA-Z0-9\-]+) C([0-9]+)"
	if [[ ${taskqueueresult} =~ $regex ]]
    then
        queueName="${BASH_REMATCH[1]}"
        CPURequirements="${BASH_REMATCH[2]}"
#        echo "${taskName}"    # cncatenate strings
#        echo "${resourceRequirements}"
		podname="renderworker"$i""
		image=$WORKERIMAGE

		$(printf "%s" "{\"apiVersion\": \"v1\",\"kind\": \"Pod\",\"metadata\": { \"name\": \""$podname"\"},\"spec\": { \"containers\": [ {\"name\": \""$podname"\",\"image\": \""$image"\", \"env\":  [{\"name\": \"BROKER_URL\",\"value\": \"amqp://guest:guest@rabbitmq-service:5672\"},{\"name\": \"QUEUE\",\"value\": \""$queueName"\"},{\"name\": \"MY_POD_NAME\",\"valueFrom\":{\"fieldRef\":{\"fieldPath\": \"metadata.name\"}}}],\"volumeMounts\": [{\"mountPath\": \"/home/shared\",\"name\": \"volume\"}], \"ports\": [{\"containerPort\": 80}] }],\"volumes\":[{\"name\": \"volume\",\"persistentVolumeClaim\":{\"claimName\": \"shared-volume\"}}],\"serviceAccount\": \"pod-creation-sa\",\"serviceAccountName\": \"pod-creation-sa\"}}" > scriptprintf)
	
		$(curl -k POST -H "Authorization: Bearer $KUBE_TOKEN" -H "Content-Type: application/json" https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_PORT_443_TCP_PORT/api/v1/namespaces/default/pods -d@scriptprintf >>/home/enqueueStdout) 

    else
        echo "${taskqueueresult} doesn't match" # this could get noisy if there are a lot of non-matching files
	fi


	i=$[$i+1]
done

echo "found taskqueue result"

#x2=$(/usr/bin/amqp-get --url=$BROKER_URL -q $taskqueueresult)
#status=$?
#echo "status: $status"
#while [ $status -eq 0 ]
#do
#x2=$(/usr/bin/amqp-get --url=$BROKER_URL -q $taskqueueresult)
#status=$?
#echo "status: $status"
#  status=$(( $x + 2 ))
#done
exit 0