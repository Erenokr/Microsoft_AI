#!/bin/sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"

if [ ! -x "$VENV_PYTHON" ]; then
    echo "Python ortamı bulunamadı. Önce setup.sh dosyasını çalıştırın."
    exit 1
fi

cd "$PROJECT_DIR"
exec "$VENV_PYTHON" main.py
