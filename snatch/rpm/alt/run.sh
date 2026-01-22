privilegedRun() 
{
  su -c "$1"
}


SNATCH_PATH="/usr/bin/snatch"

# Detecting a logged in user
if [ -n "$SUDO_USER" ]; then
    USER="$SUDO_USER"
else
    USER="$(whoami)"
fi

# Sometimes it's required to stop before start to avoid the processing issues
su $USER -c "$SNATCH_PATH/snatch_stop.sh"

# Killing the service preventing start of the rabbitmq
rabbitmqPID=$(privilegedRun "lsof -t -i :25672")
[ ! -z $rabbitmqPID ] && privilegedRun "kill -9 $rabbitmqPID" > /dev/null 2>&1

# Solving the issue ВАЖНО: пользователь "snatch_user" не прошёл проверку подлинности (по паролю)
pids=$(pgrep -f celery)
[ -n "$pids" ] && privilegedRun "kill -9 $pids" > /dev/null 2>&1

services="rabbitmq memcached"      # rabbitmq-server 
for service in $services
do
  checkService=$(systemctl status $service)
  if [[ $checkService != *"running"* ]]; then
    echo "$service is not started, starting it..."
    privilegedRun "systemctl start $service"
  else
    echo "$service is started"
  fi
done

running=""
attempt=1

su $USER -c "$SNATCH_PATH/snatch_start.sh"

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

