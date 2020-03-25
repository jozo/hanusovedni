#!/bin/bash

set -euo pipefail

# Directories for volumes
mkdir -p -m 0777 "/var/www/static"
mkdir -p -m 0777  "/var/www/media"
mkdir -p -m 0777  "/var/www/pgdata"

# Generate private key
ssh-keygen -t rsa -b 4096 -N "" -f ~/.ssh/id_rsa

docker swarm init
docker network create --driver overlay --scope swarm --attachable hanus-net
