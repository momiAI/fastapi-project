
docker network create localNetwork

docker run --name app_db -p 6432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=1 -e POSTGRES_DB=house --network=localNetwork --volume pg-data:/var/lib/postgresql/data -d postgres:17.6 

docker run --name app_redis -p 7379:6379 --network=localNetwork -d redis:latest

docker run --name app_back -p 8888:8000 --network=localNetwork fastapi-app 