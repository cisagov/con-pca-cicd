FROM node:14-alpine

WORKDIR /app
COPY ./package.json ./
COPY ./src .

RUN npm install

COPY --chown=node:node . .

WORKDIR /app/src
CMD [ "node", "server.js" ]