FROM ubuntu:18.04


RUN apt-get update && \
	apt-get install -y \
		python3.7 \
		python3-pip \
		git \
		curl \
		nodejs \
		ca-certificates \
		amqp-tools \
		python \
		dnsutils && \
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/*

#RUN apt-get install git -y

WORKDIR /home/
# move this shit to a entrypoint so i dont have to remake the image all the time
RUN git clone "https://github.com/thinhar/P9-reviewRender.git" && cd P9-reviewRender && git checkout manger-Api


RUN  curl -sL https://deb.nodesource.com/setup_9.x | bash - && \
	 curl -L https://www.npmjs.com/install.sh | sh 



RUN npm install morgan && npm install express && npm install body-parser && npm install uuid

RUN chmod +x /home/P9-reviewRender/ManagerDockerfile/Entrypoint.sh

	# testing stuff:
#RUN apt-get install nano -y


ENTRYPOINT /usr/bin/amqp-declare-queue --url=$BROKER_URL -q $QUEUE -d && /home/P9-reviewRender/ManagerDockerfile/Entrypoint.sh # call the start lisning
