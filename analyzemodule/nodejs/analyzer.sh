#!/bin/bash
taskname=$1

echo $taskname
echo "still just dumb"
#$(curl -k -X POST -d @- -H "Authorization: Bearer $KUBE_TOKEN"  -H 'Accept: application/json' -H 'Content-Type: application/json'  https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_PORT_443_TCP_PORT/api/v1/pods <<'EOF')


