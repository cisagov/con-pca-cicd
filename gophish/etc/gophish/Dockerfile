FROM gophish/gophish:latest

USER root

COPY config.json .

COPY entrypoint.sh .

RUN chmod 755 entrypoint.sh
RUN chmod 777 config.json

USER app

ENTRYPOINT ["./entrypoint.sh"]
