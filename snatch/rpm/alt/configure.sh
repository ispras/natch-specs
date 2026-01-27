SNATCH_PATH="/usr/bin/snatch"

DB_NAME="snatch_db"
DB_USER="snatch_user"

# Randomly generated password
DB_PASSWORD=$(tr -dc A-Za-z0-9 < /dev/urandom | head -c 16)
echo "$DB_PASSWORD" > /tmp/dbpas

DATADIR="/var/lib/pgsql/data"
HBA_CONF="/var/lib/pgsql/data/pg_hba.conf"

# Detecting a logged in user
if [ -n "$SUDO_USER" ]; then
	USER="$SUDO_USER"
else
	USER="$(whoami)"
fi

su -c "$SNATCH_PATH/dbinit.sh"

/home/"$USER"/.local/share/virtualenvs/snatch/env/bin/python3 $SNATCH_PATH/manage.py makemigrations Snatch
/home/"$USER"/.local/share/virtualenvs/snatch/env/bin/python3 $SNATCH_PATH/manage.py migrate

echo -e "\n\e[0;33mRemember the PostgreSQL credentials:\e[0m"
echo "==========================================="
echo -e "\e[0;33m DB name: $DB_NAME\e[0m"
echo -e "\e[0;33m Username: $DB_USER\e[0m"
echo -e "\e[0;33m Password: $DB_PASSWORD\e[0m"
echo "==========================================="

# Creating user for CI support
/home/$USER/.local/share/virtualenvs/snatch/env/bin/python3 $SNATCH_PATH/manage.py createsuperuser --username ci_bot --email ci@bot.com --noinput
echo -e "Please, note that the this token is used to perform CI API requests (it is also saved to /usr/bin/snatch/ci_token.txt)."
/home/$USER/.local/share/virtualenvs/snatch/env/bin/python3 $SNATCH_PATH/manage.py drf_create_token ci_bot | awk '{print $3}' | tee /usr/bin/snatch/ci_token.txt

echo -e "\033[32mTo use ISP RAS SNatch start \e[0m\e[1;32m$SNATCH_PATH/run.sh\e[0m\033[32m.\e[0m"

echo -e "\033[32mCheck the detailed documentation at https://github.com/ispras/natch/blob/release/docs/9_snatch.md.\e[0m"

