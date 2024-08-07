#!/bin/bash

# Executa o script dopamine_ref.py em segundo plano
nohup python3 /var/mobile/N0tA/global_ref.py -s > /var/mobile/N0tA/global_ref.out 2>&1 &
