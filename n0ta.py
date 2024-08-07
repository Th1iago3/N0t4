import json
import os
import random
import string
import datetime
import subprocess
import time
import sys

# Função para gerar um ID aleatório
def generate_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Função para criar um novo arquivo JSON com os valores iniciais
def create_json_file(directory):
    id = generate_id()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{id}-{timestamp}.json"
    filepath = os.path.join(directory, filename)
    
    data = {
        "app_version": "{dopamine_or_roothide}",
        "timestamp": timestamp,
        "- (bool)app_state": "false"
    }
    
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file)
    
    return filepath

# Função para ler o arquivo JSON
def read_json_file(filepath):
    with open(filepath, 'r') as json_file:
        return json.load(json_file)

# Função para escrever no arquivo JSON
def write_json_file(filepath, data):
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file)

# Função para atualizar o conteúdo do arquivo .sh
def update_sh_file(app_choice, active):
    sh_file = f"{app_choice}_starter.sh"
    if active:
        command = f"nohup python3 ./{app_choice}_ref.py -s > ./{app_choice}_LogCat.out 2>&1 &"
    else:
        command = f"nohup python3 ./{app_choice}_ref.py > ./{app_choice}_LogCat.out 2>&1 &"
        # Remove the log file
        log_file = f"./{app_choice}_LogCat.out"
        if os.path.exists(log_file):
            os.remove(log_file)
    
    with open(sh_file, 'w') as file:
        file.write(f"#!/bin/sh\n{command}\n")
    os.chmod(sh_file, 0o755)  # Torna o arquivo .sh executável



# Função para verificar se os arquivos estão instalados
def check_installation():
    required_files = [
        "./_verboseIndex/",
        "./global_ref.py",
        "./roothide_ref.py",
        "alljailB_starter.sh",
        "roothide_starter.sh",
        "allappstate.sh"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"{file} não encontrado.")
            break

def checod():
    required_files = [
        "./_installed.jjK"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"{file} não encontrado. Instalando Módulos...")
            os.system("sh _install.sh")
            break

# Função principal
def main():
    check_installation()
    checod()

    directory = "./_verboseIndex/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Verificar se há arquivos .json no diretório
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    if not json_files:
        filepath = create_json_file(directory)
    else:
        filepath = os.path.join(directory, json_files[0])
    
    data = read_json_file(filepath)
    
    if data["- (bool)app_state"] == "true":
        print(f"""\033[92m╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┋| App-Version: {data["app_version"]}
┋| Time: {data["timestamp"]}
┋| App-Status: Online <{data["- (bool)app_state"]}
┋| Host: localhost
╰━━━━━━━━━━\033[97m[ BOOLEAN ]\033[92m━━━━━━━━━━ """)
        input("[ + ]: 'press enter to stop dylib injection' > ")
        print("\033[91m[ + ]: '_0x5e5ad3' / exit status code '1'")
        print("\033[92m ++ !!! RESTART YOUR DEVICE TO DISABLE !!! ++")
        
        app_choice = data["app_version"]
        update_sh_file(app_choice, active=False)  # Atualiza o arquivo .sh para o estado desativado
        data["- (bool)app_state"] = "false"
    else:
        app_choice = input("[ d (dopamine) / r (Roothide) ] => ").strip().lower()
        print("[ + ]: 0x2af2b8_ / Dylib-injection is Successfully\n")
        print("[ ! ]: Restart your device To Disable...")
        
        if app_choice == 'd':
            update_sh_file('dopamine', active=True)  # Atualiza o arquivo .sh para o estado ativo
            process = subprocess.Popen(["sh", "dopamine_starter.sh"])
            data["app_version"] = "dopamine"
        elif app_choice == 'r':
            update_sh_file('roothide', active=True)  # Atualiza o arquivo .sh para o estado ativo
            process = subprocess.Popen(["sh", "roothide_starter.sh"])
            data["app_version"] = "roothide"
        
        data["- (bool)app_state"] = "true"
    
    write_json_file(filepath, data)

if __name__ == "__main__":
    main()

    sys.exit()
