FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
COPY requirements-dev.txt /app/requirements.txt
COPY requirements-test.txt /app/requirements-test.txt
RUN pip install -r requirements.txt

# Copy project
COPY ./lib /app/

CMD [ "python3", "./service.py" ]
