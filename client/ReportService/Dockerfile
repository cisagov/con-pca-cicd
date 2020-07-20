FROM node:14-alpine

WORKDIR /app
COPY ./package.json ./
COPY ./src .


RUN npm install

COPY --chown=node:node . .

CMD [ "node", "src/server.js" ]