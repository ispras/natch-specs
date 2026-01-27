#!/bin/bash

# If the Postgres data dir does not exist
if [ -d "$DATADIR" ] && [ -f "$DATADIR/PG_VERSION" ]; then
  echo "Database cluster already exists in $DATADIR"

  # Check if PostgreSQL is running
  if systemctl is-active --quiet postgresql; then
    echo "PostgreSQL is already running"

    # Check the DB existance
    if psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
        echo "Database $DB_NAME already exists, so skipping initialization"
    else
        echo "Database $DB_NAME does not exist, initializing it..."

        # Doing all the Postgres stuff
        psql -U postgres \ 
        -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$DB_NAME' AND pid <> pg_backend_pid();" \
        -c "DROP DATABASE IF EXISTS $DB_NAME;" \
        -c "DROP USER IF EXISTS $DB_USER;" \
        -c "CREATE DATABASE $DB_NAME;" \
        -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" \
        -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" \
        -c "ALTER DATABASE $DB_NAME OWNER TO $DB_USER;"
    fi
  
  else
    echo "PostgreSQL is not running. Starting..."
    systemctl enable postgresql
    systemctl start postgresql
  fi

else
  echo "Database cluster does not exist. Initializing it..."
  echo "$DB_PASSWORD" > /tmp/dbpas

  # As per https://www.altlinux.org/PostgreSQL we must create system DBs
  PGSETUP_INITDB_OPTIONS='--pgdata=/var/lib/pgsql/data --auth=trust --pwfile=/tmp/dbpas --no-instructions' /etc/init.d/postgresql initdb
  rm -f /tmp/dbpas

  echo "Starting PostgreSQL..."
  systemctl enable postgresql
  systemctl start postgresql

  # Doing all the Postgres stuff
  psql -U postgres \ 
  -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$DB_NAME' AND pid <> pg_backend_pid();" \
  -c "DROP DATABASE IF EXISTS $DB_NAME;" \
  -c "DROP USER IF EXISTS $DB_USER;" \
  -c "CREATE DATABASE $DB_NAME;" \
  -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" \
  -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" \
  -c "ALTER DATABASE $DB_NAME OWNER TO $DB_USER;"
fi

# Grabbing a currently set password and update it
currentPassword=$(cat $SNATCH_PATH/snatch/settings.py | grep PASSWORD | grep -o -P "(?<=\: \').*(?=\'\,)")
sed -i "s/$currentPassword/$DB_PASSWORD/g" $SNATCH_PATH/snatch/settings.py
