cd /app/con-pca

date

git fetch

changes=$(git rev-list HEAD..origin/develop --count)

if [ $changes -ne 0 ]; then
   echo "Need to pull"
   git pull
   date > /app/build_log.txt
   bash /app/con-pca/linux-vm-deploy.sh >> /app/build_log.txt 2> /app/build_error.txt 
else
   echo "All good"
fi
