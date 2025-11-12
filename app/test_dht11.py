import time, sys, yaml, os
from utils.sensors import DHT11Sensor, load_config

cfg = load_config(os.path.join(os.path.dirname(__file__), "config.yaml"))
pin = cfg["pins"]["dht11_data"]

print("[INFO] Leyendo DHT11. Ctrl+C para salir.\n")
try:
    dht = DHT11Sensor(pin)
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

try:
    while True:
        t, h = dht.read()
        if t is None:
            print("[WARN] Error de lectura DHT11")
        else:
            print(f"Temp: {t:.1f}°C  Hum: {h:.0f}%")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[INFO] Fin.")
