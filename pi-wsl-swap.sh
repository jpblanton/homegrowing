# Script to flip docker files since Pi needs slightly different setup

if test -f docker-compose-pi.yml; then
    mv docker-compose.yml docker-compose-wsl.yml
    mv docker-compose-pi.yml docker-compose.yml
    mv Dockerfile Dockerfile-wsl
    mv Dockerfile-pi Dockerfile
else
    mv docker-compose.yml docker-compose-pi.yml
    mv docker-compose-wsl.yml docker-compose.yml
    mv Dockerfile Dockerfile-pi
    mv Dockerfile-wsl Dockerfile
fi