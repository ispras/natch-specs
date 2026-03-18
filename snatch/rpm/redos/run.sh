SNATCH_PATH="/usr/bin/snatch"

# Detecting a logged in user
if [ -n "$SUDO_USER" ]; then
    USER="$SUDO_USER"
else
    USER="$(whoami)"
fi

# To avoid the multiple password prompts (due to "su" specifics) we are going to create a temporary script 
#   that will be executed from this script with the required privileges and that will run snatch_start.sh
echo "#!/bin/bash" > /tmp/post_run.sh

# Sometimes it's required to stop Snatch before start to avoid some processing issues
echo "$SNATCH_PATH/snatch_stop.sh" >> /tmp/post_run.sh

# Sometimes it's required to stop an existing RabbitMQ process before to avoid issues
sudo rabbitmqctl shutdown >> /tmp/post_run.sh

pids=()

# Some processes and ports may prevent a correct start of the rabbitmq
while read -r pid; do
    pids+=("$pid")
done < <(pgrep -f rabbit)

while read -r pid; do
    pids+=("$pid")
done < <(lsof -t -i :25672)

# To prevent the error: ВАЖНО: пользователь "snatch_user" не прошёл проверку подлинности (по паролю)
while read -r pid; do
    pids+=("$pid")
done < <(pgrep -f celery)

# Kill 'em all
if [ ${#pids[@]} -gt 0 ]; then
  echo "kill -9 "${pids[@]}" > /dev/null 2>&1" >> /tmp/post_run.sh
fi

services="rabbitmq-server memcached"

for service in $services
do
  # if systemctl is-active --quiet "$service"; then
  #   echo "$service is not started"
    echo "systemctl start $service" >> /tmp/post_run.sh
  # else
  #   echo "$service is already started"
  # fi
done

running=""
attempt=1

echo "sudo -u $USER $SNATCH_PATH/snatch_start.sh" >> /tmp/post_run.sh

chmod +x /tmp/post_run.sh
sudo /tmp/post_run.sh


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

