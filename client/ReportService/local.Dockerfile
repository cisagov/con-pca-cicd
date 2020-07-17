FROM buildkite/puppeteer:latest

WORKDIR /app

RUN npm install --loglevel=error
RUN npm install express --save
CMD node server.js
