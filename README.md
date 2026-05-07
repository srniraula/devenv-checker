I wrote a docker-compose.yml file that creates 3 containers:

1. nginx
2. devcheck
3. mongodb


```
docker compose up
```
It reads docker-compose.yml file and creates all containers, networks, volumes, etc. 

The reason for this is that devcheck container writes its output to mongodb database. Just a practice setup
