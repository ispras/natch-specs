SNATCH_PATH="/usr/bin/snatch"

DB_NAME="snatch_db"
DB_USER="snatch_user"

# Randomly generated password
DB_PASSWORD=$(tr -dc A-Za-z0-9 < /dev/urandom | head -c 16)

DATADIR="/var/lib/pgsql/data"

# As per "journalctl -xeu postgresql.service" we must create system DBs
if sudo [ ! -d "$DATADIR" ] && sudo [ -f "$DATADIR/PG_VERSION" ]; then
  echo "DB was already initialized"
else
  PGSETUP_INITDB_OPTIONS='-D /var/lib/pgsql/data --auth=trust' sudo -E /usr/bin/postgresql-setup --initdb
fi

sudo systemctl enable postgresql

# Check if PostgreSQL is running
if ! systemctl is-active --quiet postgresql; then
  echo "PostgreSQL is not running. Starting..."
  sudo systemctl start postgresql
fi

# Doing all the Postgres stuff
psql -U postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$DB_NAME' AND pid <> pg_backend_pid();" -c "DROP DATABASE IF EXISTS $DB_NAME;" -c "DROP USER IF EXISTS $DB_USER;" -c "CREATE DATABASE $DB_NAME;" -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" -c "ALTER DATABASE $DB_NAME OWNER TO $DB_USER;"

# Grabbing a currently set password and update it
currentPassword=$(cat $SNATCH_PATH/snatch/settings.py | grep PASSWORD | grep -o -P "(?<=\: \').*(?=\'\,)")
sudo sed -i "s/$currentPassword/$DB_PASSWORD/g" $SNATCH_PATH/snatch/settings.py

$SNATCH_PATH/manage.py makemigrations Snatch
#$SNATCH_PATH/manage.py sqlmigrate Snatch 0001
$SNATCH_PATH/manage.py migrate

echo -e "\n\e[0;33mRemember the PostgreSQL credentials:\e[0m"
echo "==========================================="
echo -e "\e[0;33m DB name: $DB_NAME\e[0m"
echo -e "\e[0;33m Username: $DB_USER\e[0m"
echo -e "\e[0;33m Password: $DB_PASSWORD\e[0m"
echo "==========================================="

echo -e "\033[32mTo use ISP RAS SNatch start \e[0m\e[1;32m$SNATCH_PATH/run.sh\e[0m\033[32m.\e[0m"

echo -e "\033[32mCheck the detailed documentation at https://github.com/ispras/natch/blob/release/docs/9_snatch.md.\e[0m"

