FROM python:3.8 as base

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

# Entrypoint
COPY ./etc/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod a+x /usr/local/bin/entrypoint.sh


# #### DEBUGGER IMAGE ####
FROM base as debug
RUN pip install ptvsd

WORKDIR /app
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
# CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess manage.py runserver 0.0.0.0:8000

# #### Production IMAGE ####
FROM base as prod

# During debugging, this entry point will be overridden. For more information, refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]