#!/bin/bash
sed -i "s/MYSQL_DATABASE/$MYSQL_DATABASE/" config.json
sed -i "s/MYSQL_USER/$MYSQL_USER/" config.json
sed -i "s/MYSQL_PASSWORD/$MYSQL_PASSWORD/" config.json
sed -i "s/MYSQL_HOST/$MYSQL_HOST/" config.json

./gophish