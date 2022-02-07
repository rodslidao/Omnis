apt-get update -y && apt-get upgrade -y
apt install net-tools
apt-get -y install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
apt-key fingerprint 0EBFCD88
add-apt-repository "deb [arch=arm64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update -y
apt-cache policy docker-ce
apt-get -y install docker-ce
exit
sudo usermod -aG docker ${USER}
sudo su
apt install python3-pip -y
apt install python3.9-venv
pip3 install docker-compose
apt install linux-modules-extra-raspi
exit