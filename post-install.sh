#!/bin/bash

#Finding pi with ethernet plugged in: ping raspberrypi.local
#Add ssh file to boot drive
#ssh pi@(address found)
#Once logged into raspberry pi change the passowrd: passwd
#Then run this script for the basics

#necessary
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install vim
sudo apt-get install git
sudo apt-get install rpi.gpio
sudo apt-get install sqlite3

#not so much

echo "yes" | ./post-install
