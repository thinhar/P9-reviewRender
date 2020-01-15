FROM ubuntu:18.04

RUN apt-get update && \
	apt-get install -y \
		#nodejs \
		libfreetype6 \
		libgl1-mesa-dev \
		libglu1-mesa \
		libxi6 \
		libxrender1 \
		ca-certificates \
		amqp-tools \
		ffmpeg \
		dnsutils && \
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/*


COPY ./encoderscript /home/script
RUN chmod +x /home/script/encoderscript.sh



#CMD /home/script/encoderscript.sh

ENTRYPOINT ["/bin/bash", "-c", "/home/script/encoderscript.sh"]
#RUN  curl -sL https://deb.nodesource.com/setup_9.x | bash - && \
#	 curl -L https://www.npmjs.com/install.sh | sh 

#RUN npm install morgan && npm install express && npm install body-parser

#COPY ./nodejs /home/nodejs


#ENTRYPOINT node /home/nodejs/server.js


# ffmpeg -framerate $framerate -start_number 1 -i /home/shared/$foldername/frame_0%03d.png -r 30 -g 90 -s $resolution -quality realtime -speed 5 -threads 2 -row-mt 1 -tile-columns 3 -frame-parallel 1 qmin 4 -qmax 48 -b:v 2000k -c:v vp9 -b:a 128k -c:a libopus -f webm "/home/shared/$foldername"






#CMD while /usr/bin/amqp-get --url=amqp://guest:guest@rabbitmq-service:5672 -q workqueue | xargs -I {} sh -c "/usr/local/blender/blender -b -noaudio /home/shared/{} -o /home/shared/frame_### -f 1"; do :; done 

# CMD /usr/bin/amqp-consume --url=$BROKER_URL -q $QUEUE -c 1 cat | xargs -I {} sh -c "/usr/local/blender/blender -b -noaudio /home/shared/{} -o /home/shared/frame_### -f 1"