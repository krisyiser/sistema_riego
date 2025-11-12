# Solución de problemas

## SD/arranque (Pi 5)
- Mensajes tipo: `bcm2712-rpi-5-b.dtb not found` u `OS does not indicate support for Raspberry Pi 5`.
  - Vuelve a grabar con **Raspberry Pi Imager** la última Raspberry Pi OS (64-bit).
- Error en actualización: `mkinitramfs ... COMPRESS: parameter not set`
  - Arreglo:
    ```bash
    echo 'COMPRESS=gzip' | sudo tee /etc/initramfs-tools/initramfs.conf
    sudo update-initramfs -u
    ```
- Evita cortes: usa **fuente oficial** y no desconectes sin `sudo poweroff`.

## GPIO / permisos
- `RuntimeError: Cannot determine SOC peripheral base address` o similares:
  - Asegúrate de estar en una **Pi real**, no en WSL. En Pi 5 usa `python3-rpi-lgpio` (apt).
- `lgpio` faltante para DHT/ Blinkа:
  - Instala dependencias:  
    ```bash
    sudo apt update
    sudo apt install -y swig python3-dev libgpiod-dev
    pip install lgpio
    ```

## DHT11
- `DHT sensor not found, check wiring`:
  - DATA a **GPIO configurado** (por defecto BCM 5), **3.3 V**, **GND**.
  - Cables cortos; aleja de bomba/relés.  
  - Prueba invertir el orden de **DATA/3.3 V** si tu módulo trae encabezado en otro orden (ver serigrafía `+ - S`).
  - Si es DHT suelto, agrega pull-up **10 kΩ** entre DATA y 3.3 V.

## Ultrasónico
- Lecturas `None` o >400 cm:
  - Verifica **divisor** de ECHO (p. ej., 5.1 k arriba, 10 k abajo).  
  - Aleja cables del motor/relés.  
  - Aumenta `timeout_s` en `Ultrasonic(...)` si tienes eco débil.

## Relés que “parpadean”
- Falta **12 V** en el lado de potencia o **masa común**.  
- Módulo activo **LOW**: un HIGH apaga; ajusta cableado y recuerda que al iniciar pueden “pulsar”.

## LCD en blanco
- Ajusta **contraste** (VO).  
- Verifica pines **RS/E/D4-D7** y que **RW esté a GND**.  
- Alimenta a **5 V**; revisa backlight.

## Ruidos / resets al activar bomba
- Diode flyback en **bomba y válvulas**.  
- Fuente separada para 12 V y Pi, con **GND común**.  
- Cables de potencia lejos de señales, añade ferrita.

## Servicio no arranca
- Revisa logs:
  ```bash
  journalctl -u riego.service -e
