#!/bin/bash
echo '[*] _installGet is true .'
sudo apt install python3
sudo apt install python3.9
python3 -m pip install pip
python3 -m pip install -r modules.txt
python3 -m pip install frida
touch _installed.jjK
echo '_installedSH=TRUE' >> _installed.jjK
echo 'isSafe=TRUE' >> _installed.jjK
echo 'Version_h=0.1.0' >> _installed.jjK
echo '[*] Ready! Done.'
clear