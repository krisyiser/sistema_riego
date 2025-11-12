#!/usr/bin/env bash
set -euo pipefail

# Bootstrap “one-liner” para una Pi recién flasheada:
# - instala paquetes base
# - corrige initramfs
# - clona (o actualiza) tu repo
# - ejecuta setup
# - instala y habilita el servicio
#
# Uso típico (una vez que subas este archivo a tu GitHub):
#   curl -fsSL https://raw.githubusercontent.com/krisyiser/sistema_riego/main/scripts/bootstrap_pi.sh | bash
#
# O si ya clonaste manualmente:  bash scripts/bootstrap_pi.sh

REPO_URL="${REPO_URL:-https://github.com/krisyiser/sistema_riego.git}"
REPO_DIR="${REPO_DIR:-$HOME/sistema_riego}"

echo "[*] Instalando paquetes base (git, curl, venv, GPIO)..."
sudo apt update
sudo apt install -y git curl python3-venv python3-pip python3-rpi-lgpio swig build-essential python3-dev libgpiod3

# Si ya tienes el repo, pull. Si no, clone.
if [ -d "$REPO_DIR/.git" ]; then
  echo "[*] Repo existente. Haciendo pull..."
  git -C "$REPO_DIR" pull --ff-only
else
  echo "[*] Clonando repo..."
  git clone "$REPO_URL" "$REPO_DIR"
fi

# Fix initramfs desde el propio repo
echo "[*] Arreglando initramfs..."
bash "$REPO_DIR/scripts/fix_initramfs.sh" || true

# Setup de Python/venv/requirements y config
echo "[*] Ejecutando setup..."
bash "$REPO_DIR/scripts/setup.sh"

# Instalar servicio systemd
echo "[*] Instalando servicio..."
bash "$REPO_DIR/scripts/install_service.sh"

echo "[OK] Bootstrap completo."
echo "    Recomendado: sudo reboot"
