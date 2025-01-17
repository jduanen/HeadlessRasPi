#!/bin/bash

#
#sudo chmod +x /etc/NetworkManager/dispatcher.d/90wifi-state-change.sh
#

if [ "$2" = "up" ] || [ "$2" = "down" ]; then
    # Your commands here
    echo "WiFi state changed to $2" >> /tmp/wifi_log.txt
    # Add your custom commands or script calls here
fi
