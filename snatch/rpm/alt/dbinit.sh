#!/bin/bash

# DB initialization

DB_NAME=$1
DB_USER=$2
DB_PASSWORD=$3

SNATCH_PATH="/usr/bin/snatch"
DATADIR="/var/lib/pgsql/data"
HBA_CONF="/var/lib/pgsql/data/pg_hba.conf"

read -s -p "Пароль суперпользователя postgres: " postgresPwd
    
# If the Postgres data dir does not exist
if [ -d "$DATADIR" ] && [ -f "$DATADIR/PG_VERSION" ]; then
  echo "Кластер БД уже существует в $DATADIR"

  # Check if PostgreSQL is running
  if systemctl is-active --quiet postgresql; then
    echo "PostgreSQL уже запущен"

    # Check the DB existance
    if PGPASSWORD=$postgresPwd psql -U postgres -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
        echo "БД $DB_NAME уже существует, инициализация пропущена"
    else
        echo "БД $DB_NAME не существует, инициализация..."

        # Doing all the Postgres stuff
        PGPASSWORD=$postgresPwd psql -U postgres -h localhost \
        -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$DB_NAME' AND pid <> pg_backend_pid();" \
        -c "DROP DATABASE IF EXISTS $DB_NAME;" \
        -c "DROP USER IF EXISTS $DB_USER;" \
        -c "CREATE DATABASE $DB_NAME;" \
        -c "CREATE USER $DB_USER WITH PASSWORD \"$DB_PASSWORD\";" \
        -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" \
        -c "ALTER DATABASE $DB_NAME OWNER TO $DB_USER;"
    fi
  
  else
    echo "PostgreSQL не запущен. Идёт запуск..."
    systemctl enable postgresql
    systemctl start postgresql
  fi

else
  echo "Кластер БД не существует. Идёт инициализация..."

  # As per https://www.altlinux.org/PostgreSQL we must create system DBs
  PGSETUP_INITDB_OPTIONS='--pgdata=/var/lib/pgsql/data --auth=trust --pwfile=/tmp/dbpas --no-instructions' /etc/init.d/postgresql initdb

  echo "Запуск PostgreSQL..."
  systemctl enable postgresql
  systemctl start postgresql

  # Doing all the Postgres stuff
  PGPASSWORD=$postgresPwd psql -U postgres \
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
