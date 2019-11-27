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
		nodejs \
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

WORKDIR /home/

RUN  curl -sL https://deb.nodesource.com/setup_9.x | bash - && \
	 curl -L https://www.npmjs.com/install.sh | sh 



RUN npm install morgan && npm install express && npm install body-parser

#RUN chmod +x /home/P9-reviewRender/ManagerDockerfile/Entrypoint.sh

COPY ./nodejs /home/nodejs
# testing stuff:
#RUN apt-get install nano -y

ENTRYPOINT node /home/nodejs/server.js
#ENTRYPOINT /home/P9-reviewRender/ManagerDockerfile/Entrypoint.sh # calls the start lisning