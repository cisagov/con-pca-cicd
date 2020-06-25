FROM node:13-alpine as build

WORKDIR /app
COPY ./AdminUI/package.json ./

RUN npm install

RUN npm install -g @angular/cli

COPY ./AdminUI .

RUN ng build --configuration production --output-path=/dist

FROM nginx:alpine

RUN apk add openssl

RUN mkdir /certs

RUN openssl req -x509 -nodes -days 365 -subj "/C=CA/ST=ID/O=INL/CN=localhost" -newkey rsa:2048 -keyout /certs/server.key -out /certs/server.crt

COPY --from=build /dist /usr/share/nginx/html
COPY ./etc/default.conf /etc/nginx/conf.d/default.conf

CMD ["/bin/sh",  "-c",  "envsubst < /usr/share/nginx/html/assets/settings.template.json > /usr/share/nginx/html/assets/settings.json && exec nginx -g 'daemon off;'"]
