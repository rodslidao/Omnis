#!/bin/bash
read -p "install host_interface service (y/n)?: " var_confirm
if [ "$var_confirm" == "y" ]; then
    cp host_interface.sh /usr/bin/host_interface.sh
    if ! [ -f /etc/systemd/system/host_interface.service ]; then
        echo "Installing ..."
        cp host_interface.service /etc/systemd/system/host_interface.service
        systemctl enable host_interface.service
        systemctl start host_interface.service
    else
        echo "host_interface service already installed, updating..."
        cat host_interface.service > /etc/systemd/system/host_interface.service
    fi
    echo "Done."
fi