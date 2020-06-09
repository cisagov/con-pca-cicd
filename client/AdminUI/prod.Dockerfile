FROM node:13-alpine as build

WORKDIR /app
COPY package.json ./

RUN npm install

COPY . .

RUN npm install -g @angular/cli

RUN ng build --configuration production --output-path=/dist

FROM nginx:alpine

COPY --from=build /dist /usr/share/nginx/html

CMD ["/bin/sh",  "-c",  "envsubst < /usr/share/nginx/html/assets/settings.template.json > /usr/share/nginx/html/assets/settings.json && exec nginx -g 'daemon off;'"]