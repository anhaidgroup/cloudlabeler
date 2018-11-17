
echo "Building new Docker image..."
docker build -t apache_labeler .

echo "Running container..."
docker run -dit --name labeler -p 8080:80 apache_labeler

echo "All done!"
