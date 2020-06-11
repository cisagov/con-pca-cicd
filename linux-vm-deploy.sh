cd /app/con-pca

cd client
/usr/local/bin/docker-compose -f prod-docker-compose.yml build
/usr/local/bin/docker-compose -f prod-docker-compose.yml up -d

cd ../controller
/usr/local/bin/docker-compose build
/usr/local/bin/docker-compose up -d


cd ../aws
/usr/local/bin/docker-compose build
/usr/local/bin/docker-compose up -d