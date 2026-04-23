#!/bin/bash

SNATCH_PATH="/usr/bin/snatch"

DB_NAME="snatch_db"
DB_USER="snatch_user"

# Randomly generated password
DB_PASSWORD=$(tr -dc A-Za-z0-9 < /dev/urandom | head -c 16)
echo "$DB_PASSWORD" > /tmp/dbpas

# Detecting a logged in user
if [ -n "$SUDO_USER" ]; then
	USER="$SUDO_USER"
else
	USER="$(whoami)"
fi

export DB_NAME DB_USER DB_PASSWORD
su -c "$SNATCH_PATH/dbinit.sh $DB_NAME $DB_USER $DB_PASSWORD"

rm -f /tmp/dbpas

echo -e "\n\e[0;33mВнимание!\e[0m Далее postgres пароли больше не требуются. Сейчас снова потребуется su пароль для настройки веб-сервисов."
su -c "$SNATCH_PATH/django.sh"

echo -e "\n\e[0;33mУчётные данные для прямого доступа к БД PostgreSQL:\e[0m"
echo "==========================================="
echo -e "\e[0;33m Имя БД: $DB_NAME\e[0m"
echo -e "\e[0;33m Пользователь: $DB_USER\e[0m"
echo -e "\e[0;33m Пароль: $DB_PASSWORD\e[0m"
echo "==========================================="

echo -e "\033[32mДля запуска ИСП РАН SNatch используйте \e[0m\e[1;32m$SNATCH_PATH/run.sh\e[0m\033[32m.\e[0m"

echo -e "\033[32mДокументация доступна по ссылке: https://github.com/ispras/natch/blob/release/docs/9_snatch.md.\e[0m"
