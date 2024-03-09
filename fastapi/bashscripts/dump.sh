#!/bin/bash

DB_NAME="postgres_db"
DB_USER="postgres_user"
DUMP_FILE="postgres_db_dump.sql"
CONTAINER_NAME="postgres"
DUMP_PATH_IN_CONTAINER="/tmp/${DUMP_FILE}"

create_dump() {
    echo "Creating dump of all tables from the PostgreSQL database inside the container..."
    docker exec $CONTAINER_NAME touch $DUMP_PATH_IN_CONTAINER
    docker exec $CONTAINER_NAME pg_dump -U $DB_USER -d $DB_NAME -f $DUMP_PATH_IN_CONTAINER
    docker cp $CONTAINER_NAME:$DUMP_PATH_IN_CONTAINER ./
    echo "Dump created successfully and copied to local machine: $DUMP_FILE"
}

restore_dump() {
    if [ -f "$DUMP_FILE" ]; then
        echo "Copying dump file from local machine to the container..."
        docker cp $DUMP_FILE $CONTAINER_NAME:$DUMP_PATH_IN_CONTAINER
        echo "Restoring tables from the dump file inside the container..."
        docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -f $DUMP_PATH_IN_CONTAINER
        echo "Restore completed successfully."
    else
        echo "Dump file does not exist: $DUMP_FILE"
    fi
}

if [[ "$1" == "--restore" ]]; then
    restore_dump
else
    create_dump
fi
