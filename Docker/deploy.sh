VERSION=$(python -c "import pkg_resources; print(pkg_resources.get_distribution('fmcapi').version)")
echo "Building and pushing docker image for fmcapi version $VERSION"
docker build --no-cache --platform linux/amd64 -t dmickels/fmcapi Docker
docker tag docker.io/dmickels/fmcapi docker.io/dmickels/fmcapi:$VERSION
docker push docker.io/dmickels/fmcapi
docker push docker.io/dmickels/fmcapi:$VERSION