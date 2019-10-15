FROM ubuntu:18.04

RUN apt-get update -y

RUN apt-get install git -y

WORKDIR /home/$username
RUN git clone "https://github.com/thinhar/P9-reviewRender.git" && cd P9-reviewRender # && git checkout branch


RUN apt-get install -y curl \
  && curl -sL https://deb.nodesource.com/setup_9.x | bash - \
  && apt-get install -y nodejs \
  && curl -L https://www.npmjs.com/install.sh | sh

RUN npm install morgan && npm install express

RUN apt-get install python3.7 -y \
	&& apt-get install python3-pip -y

#ENTRYPOINT ["/usr/local/blender/blender", "-b", "-noaudio"] # call the start lisning
