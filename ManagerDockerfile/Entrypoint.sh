# make sure we have the up to date things from git, so we dont have to create a new dockerimage every time we make changes
# since the dockerimage is static and the things on git hub is not. 
git reset --hard

# git clone "https://github.com/thinhar/P9-reviewRender.git" && cd /home/P9-reviewRender && 
git checkout manger-Api

#chmod +x /home/P9-reviewRender/nodejs/server.js
cd /home/P9-reviewRender/nodejs
node ./server.js