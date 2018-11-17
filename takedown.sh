
clear

echo "Stopping container..."
docker stop labeler

echo "Removing container..."
docker rm labeler

echo "Removing image..."
docker rmi apache_labeler

echo "All done!"
