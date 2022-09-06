#!/bin/bash
echo "waiting" > /var/run/host_signal
while inotifywait -e close_write /var/run/host_signal; do 
  signal=$(cat /var/run/host_signal)
  if [ "$signal" == "reboot" ]; then 
    echo "done _reboot" > /var/run/host_signal
    reboot
  elif [ "$signal" == "shutdown" ]; then
    echo "done _shutdown" > /var/run/host_signal
    shutdown -h now
  fi
done
