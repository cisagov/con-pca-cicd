FROM nginx:1.19.0-alpine

RUN apk add openssl
RUN mkdir /certs
RUN openssl req -x509 -nodes -days 365 -subj "/C=CA/ST=ID/O=INL/CN=localhost" -newkey rsa:2048 -keyout /certs/server.key -out /certs/server.crt

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/

RUN mkdir /code
RUN mkdir /code/static

CMD ["nginx", "-g", "daemon off;"]