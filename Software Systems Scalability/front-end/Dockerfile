FROM shawndhaliwal/seng468-frontend:latest

# make the 'app' folder the current working directory
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
#COPY package*.json ./

# install project dependencies
#RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

#serve app
CMD npm run serve

EXPOSE 8080
