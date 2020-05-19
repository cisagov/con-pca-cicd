FROM hashicorp/terraform:light

WORKDIR /app
RUN mkdir state
RUN mkdir resources
WORKDIR /app/resources
COPY ./terraform /app/resources
COPY ./terraform-entrypoint.sh /tmp/

ENTRYPOINT [ "/tmp/terraform-entrypoint.sh" ]