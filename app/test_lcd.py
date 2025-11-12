import time, os
import RPi.GPIO as GPIO
from utils.lcd import Lcd16x2
from utils.sensors import load_config

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

cfg = load_config(os.path.join(os.path.dirname(__file__), "config.yaml"))
p = cfg["pins"]

lcd = Lcd16x2(
    rs=p["lcd_rs"], e=p["lcd_e"],
    d4=p["lcd_d4"], d5=p["lcd_d5"], d6=p["lcd_d6"], d7=p["lcd_d7"],
    cols=cfg["lcd"]["cols"], rows=cfg["lcd"]["filas"]
)

lcd.print("Sistema de riego", 0, 0)
lcd.print("LCD OK :)", 1, 0)
time.sleep(3)
lcd.clear()
GPIO.cleanup()
