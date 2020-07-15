#!/bin/bash
sed -i "s/MYSQL_DATABASE/$MYSQL_DATABASE/" config.json
sed -i "s/MYSQL_USER/$MYSQL_USER/" config.json
repl=$(sed -e 's/[&\\/]/\\&/g; s/$/\\/' -e '$s/\\$//' <<<"$MYSQL_PASSWORD")
sed -i "s/MYSQL_PASSWORD/$repl/" config.json
sed -i "s/MYSQL_HOST/$MYSQL_HOST/" config.json

./gophish