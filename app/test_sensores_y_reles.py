import time, os
import RPi.GPIO as GPIO
from utils.sensors import DigitalInputs, load_config
from utils.actuators import setup_outputs, set_output

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

cfg = load_config(os.path.join(os.path.dirname(__file__), "config.yaml"))
pins = cfg["pins"]
um = cfg["umbrales"]

din = DigitalInputs(pins)
outs, fan = setup_outputs(pins, active_low=True)

print("[INFO] Probando sensores y relés. Ctrl+C para salir.\n")
i = 0
try:
    while True:
        i += 1
        suelo = din.suelo()
        tanque = din.tanque()
        luz = din.luz()
        print(f"[{i:03d}] Suelo:{suelo}  Tanque:{tanque}  Luz:{luz}")

        # parpadeo de UV para ver actividad
        set_output(outs, "uv_led", True)
        time.sleep(0.1)
        set_output(outs, "uv_led", False)

        time.sleep(0.9)
except KeyboardInterrupt:
    pass
finally:
    if fan: fan.stop()
    GPIO.cleanup()
