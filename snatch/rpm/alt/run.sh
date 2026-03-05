SNATCH_PATH="/usr/bin/snatch"

# Sometimes it's required to stop Snatch before start to avoid some processing issues
su -c "$SNATCH_PATH/snatch_stop.sh"

# Some processes and ports may prevent a correct start of the rabbitmq
pids=$(pgrep -f rabbit)
pids+=" "$(lsof -t -i :25672)

# To prevent the error: ВАЖНО: пользователь "snatch_user" не прошёл проверку подлинности (по паролю)
pids+=" "$(pgrep -f celery)

# Kill 'em all
if [ -n "$pids" ]; then
  su -c "kill -9 $pids" # > /dev/null 2>&1"
fi

services="rabbitmq memcached"      # rabbitmq-server 
services2start=""
for service in $services
do
  if systemctl is-active --quiet "$service"; then
    echo "$service is not started"
    services2start+=$service" "
  else
    echo "$service is already started"
  fi
done

if [[ ! -z $services2start ]]; then
  echo "Starting $services2start..."
  su -c "systemctl start $services2start"
fi

running=""
attempt=1

su -c "$SNATCH_PATH/snatch_start.sh"

echo "Waiting for SNatch to be started..."

while [[ -z $running ]]
do
	running=$(grep "ready." /var/log/snatch.log)
	sleep 1
	echo "... "$attempt"s."
  if [[ $attempt -eq 20 ]]; then
    echo "Warning! Celery is not ready."
    running="error"
  elif [[ ! -z $running ]]; then
    echo "SNatch is up and running."
    echo "If it did not open in browser, refresh the page after a few seconds."
  fi
	attempt=$((attempt+1))
done

