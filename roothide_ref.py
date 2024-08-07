import os
import re
import time
import shutil
import platform
import sys
import uuid
import requests
import json
import subprocess

# Caminho para o script shell
script_path = './refreshcache.sh'

# Funções e variáveis
plist_path = "/rootfs/var/mobile/Library/Application Support/Flex3/patches.plist"
txt_path = "/rootfs/var/mobile/Library/Application Support/Flex3/patches.txt"
verbose_folder = "./_verboseIndex/"
info_file = os.path.join(verbose_folder, "_infoplist")
read_puaf_file = os.path.join(verbose_folder, "_readPuafPages")
status_puaf_file = os.path.join(verbose_folder, "_statusPuaf")
apps_bundles_file = os.path.join(verbose_folder, "_AppsBundles")
_installedx = "./_installed.jjK"

# Inicializa o dicionário apps_bundles
apps_bundles = {}

def clear():
    os.system("clear")

def clean_tag(text):
    return re.sub(r'<[^>]*>', '', text)

def update_apps_bundles(bundle_id, app_name):
    with open(apps_bundles_file, 'a') as file:
        file.write(f"{bundle_id}={app_name}\n")
    apps_bundles[bundle_id] = app_name

def credentials_user_uuid():
    return str(uuid.uuid4())

def find_app(bundle_id):
    if bundle_id in apps_bundles:
        return apps_bundles[bundle_id]
    else:
        res = requests.get(f"https://itunes.apple.com/lookup?bundleId={bundle_id}&lang=pt-BR")
        if res.status_code == 200:
            data = json.loads(res.content)
            if data["results"]:
                app_name = data["results"][0]["trackName"]
            else:
                print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: '{bundle_id}' not found on LibHook")
        else:
            raise ValueError(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: '{bundle_id}' error on puafA_read: {res.status_code}")

        if app_name:
            with open(apps_bundles_file, 'a') as file:
                file.write(f"{bundle_id}={app_name}\n")
            apps_bundles[bundle_id] = app_name
            print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: '{bundle_id}' is saved on libhook.")
        return app_name

def refresh_app(app_name):
    os.system(f"killall {app_name} 2>/dev/null")

def log(message):
    print(f"[+] {message}")

def x():
    if not os.path.exists(_installedx):
        clear()
        log("_installed.jjK not installed - installing modules... ")
        os.system("sh _install.sh")
        return

def run_shell_script():
    try:
        subprocess.Popen(["sh", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"exit status code '1' / reason: {e}")

clear()
x()

if len(sys.argv) < 2:
    print("\n\n\n[+] Use: [ -r (readOnly) | -s (start) ]\n       [+]: [ -i (info) ]")
    sys.exit()

if sys.argv[1] == "-i":
   credn = credentials_user_uuid()
   iOS = platform.machine()
   vrs = platform.version()
   print(f"\n\n\n[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: 0xfffffff00a4734f0")
   print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: Machine: {iOS}")
   print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: kernel_version: {vrs}")
   print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: script_version: Bootstrap ")
   sys.exit()

if sys.argv[1] == "-r":
    iOS = platform.machine()
    vrs = platform.version()
    print(f"\n\n\n[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: Machine: {iOS}")
    print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: kernel_version: {vrs}")
    with open(plist_path, 'a') as file:
            print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: {plist_path} :200: open\n\n")
    sys.exit()

if sys.argv[1] == "-s":
   iOS = platform.machine()
   vrs = platform.version()
   print(f"\n\n\n[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: {txt_path} - OpenFile: success")
   print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: readPuafLines: 0xfffffff00789e950")
   print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: Machine: {iOS}")
   print(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: kernel_version: {vrs}")
   
   while True:
        # Executa o script shell para verificar e limpar arquivos
        run_shell_script()

        shutil.copy(plist_path, txt_path)

        with open(info_file, 'a') as file:
            file.write(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: {txt_path} :200: open")

        with open(txt_path, 'r') as file:
            lines = file.readlines()

        with open(read_puaf_file, 'a') as file:
            file.write(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: readPuafLines: {len(lines)} - :200:\n\n")
  
        with open(txt_path + ".old", 'r') as old_file:
            old_lines = old_file.readlines() if os.path.exists(txt_path + ".old") else []

        if lines != old_lines:
            changed_line = None
            for i, (new_line, old_line) in enumerate(zip(lines, old_lines)):
                if new_line != old_line:
                    changed_line = i
                    break

            if changed_line is not None:
                app_identifier_line = None
                for i in range(changed_line, 0, -1):
                    if "<key>appIdentifier</key>" in lines[i]:
                        app_identifier_line = i + 1
                        break

                if app_identifier_line is not None:
                    bundle_id = clean_tag(lines[app_identifier_line].strip())
                    app_name = find_app(bundle_id)
                    if app_name:
                        refresh_app(app_name)
                        with open(status_puaf_file, 'a') as file:
                            file.write(f"[ {time.strftime('%Y-%m-%d %H:%M:%S')} ]: :200: {app_name} -r :success:\n\n")

        shutil.copy(txt_path, txt_path + ".old")
        time.sleep(1)
else:
    print("\n\n\n[+] Use: [ -r (readOnly) | -s (start) ]\n       [+]: [ -i (info) ]")
    sys.exit()
