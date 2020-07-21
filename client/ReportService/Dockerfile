FROM node:14-alpine

WORKDIR /app
COPY ./package.json ./
COPY ./src .

RUN npm install


COPY --chown=node:node . .

COPY ./etc/entrypoint.sh /app/src/entrypoint.sh
RUN chmod 755 /app/src/entrypoint.sh

WORKDIR /app/src
ENTRYPOINT [ "/app/src/entrypoint.sh" ]