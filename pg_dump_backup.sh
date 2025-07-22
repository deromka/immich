#!/bin/bash

TIMESTAMP=$(date +\%Y-\%m-\%d_\%H-\%M-\%S)
BACKUP_DIR="/media/ironwolf/immich-postgres-dump"
FILENAME="immich_pg_dump_$TIMESTAMP.sql"
CONTAINER_NAME="immich_postgres"

docker exec -t $CONTAINER_NAME pg_dump -U postgres -F p -d postgres > "$BACKUP_DIR/$FILENAME"

