FROM --platform=linux/amd64 ubuntu:22.04
LABEL authors="Max Esser"

EXPOSE 3000/tcp

WORKDIR /frontend
COPY . .

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y nodejs npm
RUN npm install

ENTRYPOINT ["npm", "start"]