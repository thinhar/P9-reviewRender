FROM ubuntu:18.04

# get all the required tools 
RUN apt-get update && \
	apt-get install -y \
		curl \
		bzip2 \
		libfreetype6 \
		libgl1-mesa-dev \
		libglu1-mesa \
		libxi6 \
		libxrender1 \
		ca-certificates \
		amqp-tools \
		python3 \
		python3-pip \
		dnsutils && \
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install pika --upgrade


ENV BLENDER_MAJOR 2.80
ENV BLENDER_VERSION 2.80
ENV BLENDER_BZ2_URL https://mirror.clarkson.edu/blender/release/Blender$BLENDER_MAJOR/blender-$BLENDER_VERSION-linux-glibc217-x86_64.tar.bz2

# download and unpack blender
RUN mkdir /usr/local/blender && \
	curl -SL "$BLENDER_BZ2_URL" -o blender.tar.bz2 && \
	tar -jxvf blender.tar.bz2 -C /usr/local/blender --strip-components=1 && \
	rm blender.tar.bz2

COPY ./renderscript /home/script
RUN chmod +x /home/script/renderscript.sh



CMD /home/script/startpythonrender.sh






#CMD while /usr/bin/amqp-get --url=amqp://guest:guest@rabbitmq-service:5672 -q workqueue | xargs -I {} sh -c "/usr/local/blender/blender -b -noaudio /home/shared/{} -o /home/shared/frame_### -f 1"; do :; done 

# CMD /usr/bin/amqp-consume --url=$BROKER_URL -q $QUEUE -c 1 cat | xargs -I {} sh -c "/usr/local/blender/blender -b -noaudio /home/shared/{} -o /home/shared/frame_### -f 1"