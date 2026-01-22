privilegedRun() 
{
  su -c "$1"
}


SNATCH_PATH="/usr/bin/snatch"

DB_NAME="snatch_db"
DB_USER="snatch_user"

# Randomly generated password
DB_PASSWORD=$(tr -dc A-Za-z0-9 < /dev/urandom | head -c 16)
echo "$DB_PASSWORD" > /tmp/dbpas

DATADIR="/var/lib/pgsql/data"
HBA_CONF="/var/lib/pgsql/data/pg_hba.conf"

# If the Postgres data dir does not exist
if privilegedRun "[ -d \"$DATADIR\" ] && [ -f \"$DATADIR/PG_VERSION\" ]"; then
  echo "Database cluster already exists in $DATADIR"

  # Check if PostgreSQL is running
  if systemctl is-active --quiet postgresql; then
    echo "PostgreSQL is already running"

    # Check the DB existance
    if privilegedRun "psql -lqt | cut -d \| -f 1 | grep -qw \"$DB_NAME\""; then
        echo "Database $DB_NAME already exists, so skipping initialization"
    else
        echo "Database $DB_NAME does not exist, initializing it..."

        # Doing all the Postgres stuff
        psql -U postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$DB_NAME' AND pid <> pg_backend_pid();" -c "DROP DATABASE IF EXISTS $DB_NAME;" -c "DROP USER IF EXISTS $DB_USER;" -c "CREATE DATABASE $DB_NAME;" -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" -c "ALTER DATABASE $DB_NAME OWNER TO $DB_USER;"
    fi
  
  else
    echo "PostgreSQL is not running. Starting..."
    privilegedRun "systemctl enable postgresql"
    privilegedRun "systemctl start postgresql"
  fi

else
  echo "Database cluster does not exist. Initializing it..."
  echo "$DB_PASSWORD" > /tmp/dbpas

  # As per https://www.altlinux.org/PostgreSQL we must create system DBs
  PGSETUP_INITDB_OPTIONS='--pgdata=/var/lib/pgsql/data --auth=trust --pwfile=/tmp/dbpas --no-instructions' su -c "HOME='$HOME' USER='$USER' LOGNAME='/tmp/log.debug' PATH='$PATH' /etc/init.d/postgresql initdb"
  rm -f /tmp/dbpas

  echo "Starting PostgreSQL..."
  privilegedRun "systemctl enable postgresql"
  privilegedRun "systemctl start postgresql"

  # Doing all the Postgres stuff
  psql -U postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$DB_NAME' AND pid <> pg_backend_pid();" -c "DROP DATABASE IF EXISTS $DB_NAME;" -c "DROP USER IF EXISTS $DB_USER;" -c "CREATE DATABASE $DB_NAME;" -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" -c "ALTER DATABASE $DB_NAME OWNER TO $DB_USER;"
fi


# Grabbing a currently set password and update it
currentPassword=$(cat $SNATCH_PATH/snatch/settings.py | grep PASSWORD | grep -o -P "(?<=\: \').*(?=\'\,)")
privilegedRun "sed -i \"s/$currentPassword/$DB_PASSWORD/g\" $SNATCH_PATH/snatch/settings.py"

$SNATCH_PATH/manage.py makemigrations Snatch
$SNATCH_PATH/manage.py migrate

echo -e "\n\e[0;33mRemember the PostgreSQL credentials:\e[0m"
echo "==========================================="
echo -e "\e[0;33m DB name: $DB_NAME\e[0m"
echo -e "\e[0;33m Username: $DB_USER\e[0m"
echo -e "\e[0;33m Password: $DB_PASSWORD\e[0m"
echo "==========================================="

# Creating user for CI support
$SNATCH_PATH/manage.py createsuperuser --username ci_bot --email ci@bot.com --noinput
echo -e "Please, note that the this token is used to perform CI API requests (it is also saved to /usr/bin/snatch/ci_token.txt)."
$SNATCH_PATH/manage.py drf_create_token ci_bot | awk '{print $3}' | tee /usr/bin/snatch/ci_token.txt

echo -e "\033[32mTo use ISP RAS SNatch start \e[0m\e[1;32m$SNATCH_PATH/run.sh\e[0m\033[32m.\e[0m"

echo -e "\033[32mCheck the detailed documentation at https://github.com/ispras/natch/blob/release/docs/9_snatch.md.\e[0m"

