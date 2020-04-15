FROM node:13-alpine

WORKDIR /app

COPY package.json /app/package.json

RUN npm install
RUN npm install -g @angular/cli@7.3.9

ENV PATH /app/node_modules/.bin:$PATH

COPY . /app

RUN ng build

CMD ng serve --host 0.0.0.0
