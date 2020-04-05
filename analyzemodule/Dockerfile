FROM ubuntu:18.04

# get all the required tools 
RUN apt-get update && \
	apt-get install -y \
		curl \
		libfreetype6 \
		libgl1-mesa-dev \
		libglu1-mesa \
		libxi6 \
		libxrender1 \
		ca-certificates \
		amqp-tools \
		python3 \
		python3-pip \
		nodejs \
		dnsutils && \
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install pika --upgrade



# copy blender script
COPY ./BlenderScript/ /home/BlenderScript

# copy blender
COPY ./compiledBlenderFiles/blender /usr/local/blender

WORKDIR /home/

RUN  curl -sL https://deb.nodesource.com/setup_9.x | bash - && \
	 curl -L https://www.npmjs.com/install.sh | sh 



RUN npm install morgan && npm install express && npm install body-parser

#RUN chmod +x /home/P9-reviewRender/ManagerDockerfile/Entrypoint.sh

COPY ./nodejs /home/nodejs
# testing stuff:
#RUN apt-get install nano -y

ENTRYPOINT KUBE_TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token) && python3 /home/nodejs/declareTaskQueue.py && node /home/nodejs/server.js
#ENTRYPOINT /home/P9-reviewRender/ManagerDockerfile/Entrypoint.sh # calls the start lisning