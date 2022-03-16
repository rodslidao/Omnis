#!/bin/bash

# if script has executed with -y option, skip the prompt

snap install ngrok

read -p "Setup ngrok token? (y/n)?: " var_confirm
if [ "$var_confirm" == "y" ]; then
    read -p "Enter ngrok token: " token
    ngrok authtoken $token
fi


if [ -f /etc/systemd/system/ngrok.service ]; then
    echo "ngrok.service exists in /etc/systemd/system"

    # pass the contents ngrok.service to service file
    cat ngrok.service > /etc/systemd/system/ngrok.service
    systemctl enable ngrok.service

else
    read -p "Setup ngrok to start on boot (y/n)?: " var_confirm
    if [ "$var_confirm" == "y" ]; then
        cat ngrok.service > /etc/systemd/system/ngrok.service
        systemctl enable ngrok
    fi

fi
