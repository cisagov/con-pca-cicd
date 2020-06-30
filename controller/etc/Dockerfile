FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir /app/
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy project
ADD ./src /app


RUN mkdir /certs
RUN openssl req -x509 -nodes -days 365 -subj "/C=CA/ST=ID/O=INL/CN=localhost" -newkey rsa:2048 -keyout /certs/server.key -out /certs/server.crt

# Entrypoint
COPY ./etc/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod a+x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
