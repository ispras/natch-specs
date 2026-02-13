SNATCH_PATH="/usr/bin/snatch"

# Detecting a logged in user
if [ -n "$SUDO_USER" ]; then
    USER="$SUDO_USER"
else
    USER="$(whoami)"
fi

# Sometimes it's required to stop an existing RabbitMQ process before to avoid issues
sudo rabbitmqctl shutdown

services="rabbitmq-server memcached"
for service in $services
do
  checkService=$(systemctl status $service)
  if [[ $checkService != *"running"* ]]; then
    echo "$service is not started, starting it..."
    sudo systemctl start $service
  else
    echo "$service is started"
  fi
done

running=""
attempt=1

sudo -u $USER $SNATCH_PATH/snatch_start.sh no-autorun-browser

echo "Waiting for SNatch to be started..."

running=0

while [[ $running -ne 200 ]] && [[ $running -ne 302 ]]; do
  running=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000")
	sleep 1
	echo "... "$attempt"s."
  if [[ $attempt -eq 10 ]]; then
    echo "It looks like Snatch still does not work. Please share /var/log/snatch.log with Natch team."
    running="error"
  elif [[ $running -eq 200 ]] || [[ $running -eq 302 ]]; then
    echo "SNatch is up and running."
  fi
	attempt=$((attempt+1))
done

