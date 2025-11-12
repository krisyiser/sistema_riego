#!/usr/bin/env bash
set -euo pipefail

# Arregla problemas recurrentes al generar initramfs en Pi 5 (COMPRESS/MODULES).
# Es seguro ejecutarlo varias veces.

CONF="/etc/initramfs-tools/initramfs.conf"

echo "[*] Aplicando fix de initramfs en ${CONF}..."
sudo mkdir -p /etc/initramfs-tools
if [ ! -f "$CONF" ]; then
  echo "[*] Creando $CONF"
  echo "COMPRESS=gzip" | sudo tee "$CONF" >/dev/null
  echo "MODULES=most"  | sudo tee -a "$CONF" >/dev/null
else
  # COMPRESS=gzip
  if grep -q '^COMPRESS=' "$CONF"; then
    sudo sed -i 's/^COMPRESS=.*/COMPRESS=gzip/g' "$CONF"
  else
    echo "COMPRESS=gzip" | sudo tee -a "$CONF" >/dev/null
  fi
  # MODULES=most
  if grep -q '^MODULES=' "$CONF"; then
    sudo sed -i 's/^MODULES=.*/MODULES=most/g' "$CONF"
  else
    echo "MODULES=most" | sudo tee -a "$CONF" >/dev/null
  fi
fi

echo "[*] Regenerando initramfs (puede tardar un poco)..."
if sudo update-initramfs -u; then
  echo "[OK] initramfs actualizado."
else
  echo "[!] Aviso: hubo warnings. Si no ves 'failed', normalmente es seguro continuar."
fi
