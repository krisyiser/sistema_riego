import time, os
import RPi.GPIO as GPIO
from utils.sensors import Ultrasonic, load_config

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

cfg = load_config(os.path.join(os.path.dirname(__file__), "config.yaml"))
u = Ultrasonic(cfg["pins"]["ultra_trig"], cfg["pins"]["ultra_echo"])

print("[INFO] Leyendo distancia (cm). Ctrl+C para salir.\n")
try:
    while True:
        d = u.distance_cm()
        print(f"Dist: {d:.1f} cm" if d else "Dist: --")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
