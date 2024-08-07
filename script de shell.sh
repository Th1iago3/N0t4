#!/bin/bash

# Verifica os argumentos
if [ $# -lt 2 ]; then
    echo "Uso: $0 -r [on|off] | -d [on|off]"
    exit 1
fi

# Função para atualizar o arquivo roothide_starter.sh
update_roothide() {
    if [ "$1" = "on" ]; then
        echo "nohup python3 ./roothide_ref.py -s > /var/mobile/N0tA/roothide_LogCat.out 2>&1 &" > "./roothide_starter.sh"
    elif [ "$1" = "off" ]; then
        echo "nohup python3 ./roothide_ref.py > ./roothide_LogCat.out 2>&1 &" > "./roothide_starter.sh"
    else
        echo "Argumento inválido para roothide: $1"
        exit 1
    fi
}

# Função para atualizar o arquivo dopamine_starter.sh
update_dopamine() {
    if [ "$1" = "on" ]; then
        echo "nohup python3 ./dopamine_ref.py -s > ./dopamine_LogCat.out 2>&1 &" > "/var/mobile/N0tA/dopamine_starter.sh"
    elif [ "$1" = "off" ]; then
        echo "nohup python3 ./dopamine_ref.py > ./dopamine_LogCat.out 2>&1 &" > "/var/mobile/N0tA/dopamine_starter.sh"
    else
        echo "Argumento inválido para dopamine: $1"
        exit 1
    fi
}

# Processa os argumentos
while getopts "roothide:dopamine:" opt; do
    case $opt in
        roothide)
            update_roothide "$OPTARG"
            ;;
        dopamine)
            update_dopamine "$OPTARG"
            ;;
        \?)
            echo "Opção inválida: -$OPTARG"
            exit 1
            ;;
        :)
            echo "Opção -$OPTARG requer um argumento."
            exit 1
            ;;
    esac
done