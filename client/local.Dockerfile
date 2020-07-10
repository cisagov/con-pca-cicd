FROM node:13-alpine

WORKDIR /app

COPY ./AdminUI/package.json /app/package.json

RUN apk add -U --no-cache --allow-untrusted udev ttf-freefont chromium git

RUN npm install --loglevel=error
RUN npm install -g @angular/cli@9.1.8
RUN npm install puppeteer-core --silent

ENV PATH /app/node_modules/.bin:$PATH

COPY ./AdminUI /app

RUN ng build

CMD ng serve --host 0.0.0.0
