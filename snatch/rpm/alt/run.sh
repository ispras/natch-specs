SNATCH_PATH="/usr/bin/snatch"

# To avoid the multiple password prompts (due to "su" specifics) we are going to create a temporary script 
#   that will be executed from this script with the required privileges and that will run snatch_start.sh
echo "#!/bin/bash" > /tmp/post_run.sh

# Sometimes it's required to stop Snatch before start to avoid some processing issues
echo "$SNATCH_PATH/snatch_stop.sh" >> /tmp/post_run.sh

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

services="rabbitmq memcached"      # rabbitmq-server 
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

echo "$SNATCH_PATH/snatch_start.sh" >> /tmp/post_run.sh

chmod +x /tmp/post_run.sh
su -c "/tmp/post_run.sh"

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

