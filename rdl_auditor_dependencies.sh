#!/bin/bash
sed -i -e 's/\r$//' auditor_dependencies.sh #run if script crashes
#if tkcalendar crashes run
sudo add-apt-repository ppa:j-4321-i/ppa
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install numpy
sudo pip3 install opencv-python
sudo pip3 install rq
sudo pip3 install tkcalendar
sudo pip3 install pillow
sudo pip3 install urllib3
sudo apt-get install python3-pil
sudo apt-get install python3-pil.imagetk
sudo add-apt-repository ppa:j-4321-i/ppa
#Install to resize image
#sudo apt-get install imagemagick
#convert my_logo.png -resize 200x200 my_logo1.png
