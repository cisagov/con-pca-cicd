#!/bin/sh
sed -i "s/__BROWSERLESS_ENDPOINT__/$BROWSERLESS_ENDPOINT/" app/generate_pdf.js
sed -i "s/__WEB_ENDPOINT__/$WEB_ENDPOINT/" app/generate_pdf.js
node server.js