#!/bin/bash

url=$1
requestedUserAgent=$2
deleteCookies=$3
location=$4
pcUsername=$(cat /etc/username)

rm /tmp/ready
# Marks the container as busy, as we're now getting started on our computations. We won't receive new HTTP requests until we add the file back.

echo $url $requestedUserAgent $deleteCookies $location $(cat /etc/ipvanish/email) $(cat /etc/ipvanish/password) $pcUsername > /home/$pcUsername/arguments
sudo -u $pcUsername -i /bin/bash - <<-'EOF'
	~/P7-DimensionalShopping/Backend/query.py $(cat arguments)
EOF
# We impersonate the user $pcUsername (which ensures that our home directory ~ points to the correct location)

touch /tmp/ready