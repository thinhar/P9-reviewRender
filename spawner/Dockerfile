FROM ubuntu:18.04

# get all the required tools 
RUN apt-get update && \
	apt-get install -y \
		curl \
		ca-certificates \
		amqp-tools \
		python3 \
		python3-pip \
		dnsutils && \
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install pika --upgrade

COPY ./spawningScript /home/script
RUN chmod +x /home/script/spawnerScript.sh

CMD /home/script/spawnerScript.sh






#CMD while /usr/bin/amqp-get --url=amqp://guest:guest@rabbitmq-service:5672 -q workqueue | xargs -I {} sh -c "/usr/local/blender/blender -b -noaudio /home/shared/{} -o /home/shared/frame_### -f 1"; do :; done 

# CMD /usr/bin/amqp-consume --url=$BROKER_URL -q $QUEUE -c 1 cat | xargs -I {} sh -c "/usr/local/blender/blender -b -noaudio /home/shared/{} -o /home/shared/frame_### -f 1"