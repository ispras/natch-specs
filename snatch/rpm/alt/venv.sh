#!/bin/bash

# Virtual environment actions

SNATCH_PATH="/usr/bin/snatch"

echo "Activating Python virtual environment"
cd /opt/snatch/venv/

. env/bin/activate
python3 $SNATCH_PATH/manage.py makemigrations Snatch
python3 $SNATCH_PATH/manage.py migrate

# Creating user for CI support
python3 $SNATCH_PATH/manage.py createsuperuser --username ci_bot --email ci@bot.com --noinput

echo -e "Please, note that the this token is used to perform CI API requests (it is also saved to /usr/bin/snatch/ci_token.txt)."
python3 $SNATCH_PATH/manage.py drf_create_token ci_bot | awk '{print $3}' | tee /usr/bin/snatch/ci_token.txt
