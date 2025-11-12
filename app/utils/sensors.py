import time
import os
import yaml

import RPi.GPIO as GPIO

# DHT11 (Blinka)
try:
    import adafruit_dht
    import board  # provisto por Blinka
    _HAVE_DHT = True
except Exception:
    _HAVE_DHT = False


def load_config(path=None):
    path = path or os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class DigitalInputs:
    """Lecturas digitales simples (DO) de suelo, tanque, LDR."""
    def __init__(self, pins):
        self.p_suelo = pins["suelo_do"]
        self.p_tanque = pins["tanque_do"]
        self.p_ldr = pins["ldr_do"]
        GPIO.setup(self.p_suelo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.p_tanque, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.p_ldr, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def suelo(self):   # 0/1
        return GPIO.input(self.p_suelo)

    def tanque(self):  # 0/1
        return GPIO.input(self.p_tanque)

    def luz(self):     # 0/1
        return GPIO.input(self.p_ldr)


class DHT11Sensor:
    """DHT11: temperatura/humedad. Usa Adafruit + Blinka."""
    def __init__(self, data_pin_bcm):
        if not _HAVE_DHT:
            raise RuntimeError("adafruit_dht/blinka no disponibles")
        # Mapa rápido BCM->board:
        bcm2board = {
            2: board.D2, 3: board.D3, 4: board.D4, 5: board.D5, 6: board.D6,
            7: board.D7, 8: board.D8, 9: board.D9, 10: board.D10, 11: board.D11,
            12: board.D12, 13: board.D13, 16: board.D16, 17: board.D17,
            18: board.D18, 19: board.D19, 20: board.D20, 21: board.D21,
            22: board.D22, 23: board.D23, 24: board.D24, 25: board.D25,
            26: board.D26, 27: board.D27
        }
        if data_pin_bcm not in bcm2board:
            raise ValueError(f"Pin BCM {data_pin_bcm} no mapeado en este helper.")
        self._dht = adafruit_dht.DHT11(bcm2board[data_pin_bcm], use_pulseio=False)

    def read(self):
        """Devuelve (temp_c, hum) o (None, None) si la lectura falla."""
        try:
            t = self._dht.temperature
            h = self._dht.humidity
            if t is None or h is None:
                return None, None
            return float(t), float(h)
        except Exception:
            return None, None


class Ultrasonic:
    """HC-SR04 con divisor al Echo para 3V3. Distancia en cm."""
    def __init__(self, trig_bcm, echo_bcm, timeout_s=0.03):
        self.p_trig = trig_bcm
        self.p_echo = echo_bcm
        self.timeout = timeout_s
        GPIO.setup(self.p_trig, GPIO.OUT)
        GPIO.setup(self.p_echo, GPIO.IN)
        GPIO.output(self.p_trig, GPIO.LOW)
        time.sleep(0.05)

    def distance_cm(self, samples=3):
        vals = []
        for _ in range(samples):
            # trigger 10us
            GPIO.output(self.p_trig, GPIO.HIGH)
            time.sleep(10e-6)
            GPIO.output(self.p_trig, GPIO.LOW)

            # esperar pulso
            t0 = time.time()
            while GPIO.input(self.p_echo) == 0:
                if time.time() - t0 > self.timeout:
                    break
            start = time.time()

            t1 = time.time()
            while GPIO.input(self.p_echo) == 1:
                if time.time() - t1 > self.timeout:
                    break
            end = time.time()

            dur = end - start
            # velocidad sonido ~34300 cm/s; ida y vuelta -> /2
            d = (dur * 34300) / 2.0
            vals.append(d)
            time.sleep(0.02)
        # mediana para suavizar
        vals = sorted([v for v in vals if 0.5 <= v <= 400])
        if not vals:
            return None
        return vals[len(vals)//2]
