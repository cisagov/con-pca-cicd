FROM node:13-alpine as build

WORKDIR /app
COPY ./AdminUI/package.json ./

RUN npm install

RUN npm install -g @angular/cli

COPY ./AdminUI .

RUN ng build --configuration production --output-path=/dist

FROM nginx:alpine

COPY --from=build /dist /usr/share/nginx/html
COPY ./etc/default.conf /etc/nginx/conf.d/default.conf
RUN mkdir /certs
# COPY ./etc/server.crt /certs/server.crt
# COPY ./etc/server.key /certs/server.key

CMD ["/bin/sh",  "-c",  "envsubst < /usr/share/nginx/html/assets/settings.template.json > /usr/share/nginx/html/assets/settings.json && exec nginx -g 'daemon off;'"]
