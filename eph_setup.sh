#!/bin/bash

sudo apt-get update
yes | sudo apt-get upgrade
sudo apt-get -y install  libi2c-dev i2c-tools python-smbus libfuse-dev python-imaging

#git clone https://github.com/Percheron-Electronics/gratis
git clone https://github.com/mlagerberg/gratis
cd gratis/PlatformWithOS
make rpi
sudo make rpi-install

echo "Please reboot to finish installation"

