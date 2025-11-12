import os, time, datetime as dt
import RPi.GPIO as GPIO
import yaml

from utils.sensors import load_config, DigitalInputs, DHT11Sensor, Ultrasonic
from utils.actuators import setup_outputs, set_output, pulse
from utils.lcd import Lcd16x2


def now_hhmm():
    return dt.datetime.now().strftime("%H:%M")


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    cfg = load_config(os.path.join(os.path.dirname(__file__), "config.yaml"))
    pins, um = cfg["pins"], cfg["umbrales"]

    # --- IO ---
    din = DigitalInputs(pins)
    outs, fan = setup_outputs(pins, active_low=True)

    # DHT11 (opcional: puede fallar si no está cableado aún)
    dht = None
    try:
        dht = DHT11Sensor(pins["dht11_data"])
    except Exception:
        dht = None

    ultra = Ultrasonic(pins["ultra_trig"], pins["ultra_echo"])

    # LCD
    lcd = Lcd16x2(
        rs=pins["lcd_rs"], e=pins["lcd_e"],
        d4=pins["lcd_d4"], d5=pins["lcd_d5"], d6=pins["lcd_d6"], d7=pins["lcd_d7"],
        cols=cfg["lcd"]["cols"], rows=cfg["lcd"]["filas"]
    )

    last_riego_z1 = 0
    cool_z1 = cfg["riegos"]["zona1"]["cooldown_s"]
    dur_z1 = cfg["riegos"]["zona1"]["duracion_s"]
    prog_z2 = cfg["riegos"]["zona2"]["programado"]
    dur_z2 = cfg["riegos"]["zona2"]["duracion_s"]

    lcd.print("Riego iniciado", 0, 0)
    time.sleep(1)
    lcd.clear()

    try:
        while True:
            suelo = din.suelo()
            tanque = din.tanque()
            luz = din.luz()

            t, h = (None, None)
            if dht:
                t, h = dht.read()

            dist = ultra.distance_cm() or 0

            # --- LCD línea 1: sensores básicos
            l1 = f"T:{'-' if t is None else int(t)}C H:{'-' if h is None else int(h)}% D:{int(dist):3d}cm"
            lcd.print(l1.ljust(16)[:16], 0, 0)

            # --- ZONA 1 (sensores)
            tanque_ok = (tanque != um["tanque_min"])
            suelo_seco = (suelo == um["suelo_seco"])

            do_riego_z1 = tanque_ok and suelo_seco and (time.time() - last_riego_z1 > cool_z1)

            if dht and (t is not None and h is not None):
                # control sencillo de ventilador por temperatura
                if t > um["temp_max"] and fan:
                    fan.ChangeDutyCycle(70)
                else:
                    if fan:
                        fan.ChangeDutyCycle(0)

            if do_riego_z1:
                lcd.print("Z1: RIEGO      ", 1, 0)
                set_output(outs, "bomba", True)
                set_output(outs, "valvula1", True)
                time.sleep(dur_z1)
                set_output(outs, "valvula1", False)
                set_output(outs, "bomba", False)
                last_riego_z1 = time.time()
            else:
                # --- ZONA 2 (programado)
                hhmm = now_hhmm()
                if hhmm in prog_z2 and tanque_ok:
                    lcd.print("Z2: RIEGO      ", 1, 0)
                    set_output(outs, "bomba", True)
                    set_output(outs, "valvula2", True)
                    time.sleep(dur_z2)
                    set_output(outs, "valvula2", False)
                    set_output(outs, "bomba", False)
                    time.sleep(60)  # evita repetir dentro del mismo minuto
                else:
                    # estado idle en LCD
                    estado = "OK" if tanque_ok else "SIN AGUA"
                    lcd.print(f"Z1:{'SECO' if suelo_seco else 'HUM.'} {estado}".ljust(16)[:16], 1, 0)

            # LED UV simple según luz
            set_output(outs, "uv_led", bool(luz == um["luz_min"]))

            time.sleep(1.0)

    except KeyboardInterrupt:
        pass
    finally:
        if fan: fan.stop()
        set_output(outs, "uv_led", False)
        for k in ("bomba", "valvula1", "valvula2"):
            if k in outs: set_output(outs, k, False)
        GPIO.cleanup()


if __name__ == "__main__":
    main()
