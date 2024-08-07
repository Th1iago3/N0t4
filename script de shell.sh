#!/bin/sh

# Define os caminhos dos arquivos
info_file="./_verboseIndex/_infoplist"
read_puaf_file="./readPuafPages"
status_puaf_file="./_statusPuaf"


# Captura O Tempo Atual
get_current_time() {
    date +"[%Y-%m-%d %H:%M:%S]"
}

# Tamanho máximo permitido em bytes (1 MB)
max_size=$((1 * 1024 * 1024))

# Função para verificar e limpar arquivo se exceder o tamanho
check_and_clear() {
    local file=$1
    local file_size=$(stat -c%s "$file")

    if [ "$file_size" -gt "$max_size" ]; then
        echo "[ $(get_current_time) ]: Rebuilding IconCache"
        > "$file"  # Limpa o conteúdo do arquivo
    fi
}

# Verifica e limpa os arquivos
check_and_clear "$info_file"
check_and_clear "$read_puaf_file"
check_and_clear "$status_puaf_file"
