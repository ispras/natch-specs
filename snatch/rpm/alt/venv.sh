#!/bin/bash

# Virtual environment creation

echo "Creating Python virtual environment"
mkdir -p /opt/snatch/venv/
chmod 755 /opt/snatch/venv/

if [ -d env ]; then
	echo "Removing the existing Python environment"
	rm -rf env
fi

echo "Activating Python virtual environment"
cd /opt/snatch/venv/
su -c "python3 -m venv env"
su -c ". env/bin/activate"

su -c "/opt/snatch/venv/env/bin/pip3 install --upgrade pip"

# This is from the beginning of the requirements.txt
su -c "/opt/snatch/venv/env/bin/pip3 install --upgrade celery-progress~=0.1.2 celery~=5.2.6"

# Grabbing the last requirements from the file
REQUIREMENTSPLACEHOLDER

# Separate vmi (v4.0)
su -c "/opt/snatch/venv/env/bin/pip3 install /usr/bin/snatch/vmi"
rm -rf /usr/bin/snatch/vmi
