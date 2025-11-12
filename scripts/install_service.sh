#!/usr/bin/env bash
set -euo pipefail

# Instala/activa el servicio systemd que arranca el programa principal al boot.

SERVICE_NAME="riego.service"
SRC="${SRC:-$HOME/sistema_riego/services/$SERVICE_NAME}"
DST="/etc/systemd/system/$SERVICE_NAME"

if [ ! -f "$SRC" ]; then
  echo "[ERROR] No existe $SRC"
  exit 1
fi

echo "[*] Instalando servicio en $DST ..."
sudo cp "$SRC" "$DST"
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"

echo "[*] Puedes iniciar ahora el servicio con:"
echo "    sudo systemctl start $SERVICE_NAME"
echo "[*] Logs en vivo:"
echo "    journalctl -u $SERVICE_NAME -f"
