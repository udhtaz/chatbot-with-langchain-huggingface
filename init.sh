clear

export $(grep -v '^#' .env | xargs)

docker build -t rag_api:1.00 .
docker image ls
docker image rm -f $(docker images -f dangling=true -q)
docker run -p 80:80 rag_api:1.00