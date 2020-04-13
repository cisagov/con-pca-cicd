FROM nginx:latest

RUN apt update

RUN apt install -y \
    python3-acme \
    python3-certbot \
    python3-mock \
    python3-openssl \
    python3-pkg-resources \
    python3-pyparsing \
    python3-zope.interface

RUN apt install python3-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY config.conf /etc/nginx/conf.d/

CMD ["nginx", "-g", "daemon off;"]