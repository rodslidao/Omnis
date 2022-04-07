#!/bin/bash

# if script has executed with -y option, skip the prompt

snap install ngrok

read -p "Setup ngrok token? (y/n)?: " var_confirm
if [ "$var_confirm" == "y" ]; then
    read -p "Enter ngrok token: " token
    ngrok authtoken $token
fi

read -p "Setup ngrok to start on boot (y/n)?: " var_confirm
if [ "$var_confirm" == "y" ]; then
    if ! [ -f /etc/systemd/system/ngrok.service ]; then
        echo "Installing ngrok service..."
        cp ngrok.service /etc/systemd/system/ngrok.service
        systemctl enable ngrok.service
        systemctl start ngrok.service
    else
        echo "ngrok service already installed, updating..."
        cat ngrok.service > /etc/systemd/system/ngrok.service
    fi
    if ! [ -f /etc/systemd/system/dump_ngrok.service ]; then
        echo "Installing ngrok dump service..."
        cp dump_ngrok.service /etc/systemd/system/dump_ngrok.service
        systemctl enable dump_ngrok.service
        systemctl start dump_ngrok.service
    else
        echo "ngrok dump service already installed, updating..."
        cat dump_ngrok.service > /etc/systemd/system/dump_ngrok.service
    fi
    systemctl daemon-reload
fi
