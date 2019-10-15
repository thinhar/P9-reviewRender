FROM ubuntu:18.04

RUN apt-get update -y

RUN apt-get install git -y

WORKDIR /home/
# move this shit to a entrypoint so i dont have to remake the image all the time
RUN git clone "https://github.com/thinhar/P9-reviewRender.git" && cd P9-reviewRender && git checkout manger-Api


RUN apt-get install -y curl \
  && curl -sL https://deb.nodesource.com/setup_9.x | bash - \
  && apt-get install -y nodejs \
  && curl -L https://www.npmjs.com/install.sh | sh

RUN npm install morgan && npm install express && npm install body-parser

RUN apt-get install python3.7 -y \
	&& apt-get install python3-pip -y

RUN chmod +x /home/P9-reviewRender/ManagerDockerfile/Entrypoint.sh

	# testing stuff:
RUN apt-get install nano -y


ENTRYPOINT /home/P9-reviewRender/ManagerDockerfile/Entrypoint.sh # call the start lisning
