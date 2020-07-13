FROM gophish/gophish:latest

USER root

RUN apt update -y
RUN apt install openssl -y

RUN mkdir /certs
RUN openssl req -x509 -nodes -days 365 -subj "/C=CA/ST=ID/O=INL/CN=localhost" -newkey rsa:2048 -keyout /certs/server.key -out /certs/server.crt

RUN chmod 755 /certs/server.crt
RUN chmod 755 /certs/server.key

COPY config.json .

COPY entrypoint.sh .

RUN chmod 755 entrypoint.sh
RUN chmod 777 config.json

USER app

ENTRYPOINT ["./entrypoint.sh"]
