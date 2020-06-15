FROM node:13-alpine as build

WORKDIR /app
COPY ./AdminUI/package.json ./

RUN npm install

COPY ./AdminUI .

RUN npm install -g @angular/cli

RUN ng build --configuration production --output-path=/dist

FROM nginx:alpine

COPY --from=build /dist /usr/share/nginx/html
COPY ./etc/default.conf /etc/nginx/conf.d/default.conf

CMD ["/bin/sh",  "-c",  "envsubst < /usr/share/nginx/html/assets/settings.template.json > /usr/share/nginx/html/assets/settings.json && exec nginx -g 'daemon off;'"]
