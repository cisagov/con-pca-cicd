FROM node:14-alpine

ADD package*.json ./

WORKDIR /app
COPY ./src .

USER node

RUN npm install

COPY --chown=node:node . .

CMD [ "node", "server.js" ]