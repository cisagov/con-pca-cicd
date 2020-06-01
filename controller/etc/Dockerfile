FROM python:3.8 as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
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
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# #### DEBUGGER IMAGE ####
# from base as debug
# run pip install ptvsd

# WORKDIR /app
# cmd python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiporcess -m /usr/local/bin/entrypoint.sh

# #### Production IMAGE ####
# from base as prod
# During debugging, this entry point will be overridden. For more information, refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]