
docker network create localNetwork

docker run --name app_db  \
    -p 6432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=1 \ 
    -e POSTGRES_DB = house \
    --network=localNetwork \
    --volume pg-data:/var/lib/postgresql/data \
    -d postgres:17.6

docker run --name app_db -d postgres:17.6 -p 6432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=1 e POSTGRES_DB = house --network=localNetwork --volume pg-data:/var/lib/postgresql/data 