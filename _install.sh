#!/bin/bash
echo '[*] _installGet is true .'
sudo apt install python3
sudo apt install python3.9
python3 get-pip.py
pip3 install -r modules.txt
touch _installed.jjK
echo '_installedSH=TRUE' >> _installed.jjK
echo 'isSafe=TRUE' >> _installed.jjK
echo 'Version_h=0.1.0' >> _installed.jjK
echo '[*] Ready! Done.'
clear
