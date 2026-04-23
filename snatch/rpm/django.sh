#!/bin/bash

# Virtual environment actions to prepare Django stuff

SNATCH_PATH="/usr/bin/snatch"

echo "Активация виртуальной среды Python"
cd /opt/snatch/venv/

. env/bin/activate
python3 $SNATCH_PATH/manage.py makemigrations Snatch
python3 $SNATCH_PATH/manage.py migrate

# Creating user for CI support
python3 $SNATCH_PATH/manage.py createsuperuser --username ci_bot --email ci@bot.com --noinput

echo -e "Внимание! Этот токен может быть использован для CI API запросов (он также сохранён в /usr/bin/snatch/ci_token.txt):"
python3 $SNATCH_PATH/manage.py drf_create_token ci_bot | awk '{print $3}' | tee /usr/bin/snatch/ci_token.txt
