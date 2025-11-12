#!/usr/bin/env bash
set -euo pipefail

# Instala dependencias, crea venv, instala requirements y genera config por defecto
# para el proyecto de riego. Se asume que estás en una Raspberry Pi.

PROJ="${PROJ:-$HOME/sistema_riego}"

echo "[*] Actualizando paquetes..."
sudo apt update
# Permitimos que full-upgrade falle sin romper el script (a veces muestra warnings inofensivos)
sudo apt full-upgrade -y || true

echo "[*] Instalando dependencias del sistema..."
# - python3-rpi-lgpio: soporte GPIO estilo RPi.GPIO (útil para scripts que lo usen)
# - libgpiod3: backend gpiod moderno (Blinka en Pi5)
# - swig/build-essential/python3-dev: para compilar módulos tipo lgpio si hace falta
# - git, curl por si no están
sudo apt install -y \
  python3-venv python3-pip python3-dev \
  python3-rpi-lgpio libgpiod3 \
  swig build-essential git curl

echo "[*] Armonizando initramfs (por si las dudas)..."
bash "$PROJ/scripts/fix_initramfs.sh" || true

echo "[*] Creando entorno virtual..."
mkdir -p "$PROJ"
cd "$PROJ"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

echo "[*] Instalando requirements de Python..."
if [ -f "$PROJ/app/requirements.txt" ]; then
  pip install -r "$PROJ/app/requirements.txt"
else
  echo "[WARN] No existe app/requirements.txt. Saltando instalación de Python."
fi

# Generar config.yaml por defecto si no existe
CFG="$PROJ/app/config.yaml"
if [ ! -f "$CFG" ]; then
  echo "[*] Creando config.yaml por defecto..."
  cat > "$CFG" <<'YAML'
# Config Pi (BCM) y rangos básicos — AJUSTA a tu cableado real
pins:
  bomba:         17
  valvula1:      22
  valvula2:      23
  suelo_do:      27
  tanque_do:     26
  ldr_do:        24

  dht11_data:     5

  fan_pwm:        6

  ultra_trig:    12
  ultra_echo:    16

  lcd_rs:        25
  lcd_e:         19
  lcd_d4:         4
  lcd_d5:        13
  lcd_d6:        20
  lcd_d7:        21

  uv_led:        18

umbrales:
  suelo_seco:   1      # 1=seco (según módulo). Si tu sensor es inverso, cámbialo.
  luz_min:      1      # 1=poca luz (DO alto). Ajusta a tu divisor/umbral.
  tanque_min:   1      # 1=tanque vacío (DO alto).
  temp_max:     30
  temp_min:     12
  hr_min:       35
  hr_max:       75

riegos:
  zona1:
    duracion_s: 10
    cooldown_s: 300
  zona2:
    programado: ["08:00", "13:00", "18:00"]

ultra:
  min_cm:       5
  max_cm:       200

lcd:
  filas:        2
  cols:         16
YAML
fi

echo "[OK] Setup completado en $PROJ"
echo "     Activa el venv con:  source $PROJ/.venv/bin/activate"
