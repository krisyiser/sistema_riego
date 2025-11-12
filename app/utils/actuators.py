import time
import RPi.GPIO as GPIO


def setup_outputs(pins, active_low=True):
    """Inicializa pines de salida (relés, LEDs, ventilador PWM)."""
    outputs = {}
    for name in ("bomba", "valvula1", "valvula2", "uv_led"):
        if name in pins:
            pin = pins[name]
            GPIO.setup(pin, GPIO.OUT)
            # relés LOW-trigger por defecto -> apaga en HIGH
            GPIO.output(pin, GPIO.HIGH if active_low else GPIO.LOW)
            outputs[name] = (pin, active_low)

    # ventilador PWM (opcional)
    fan_pwm = None
    if "fan_pwm" in pins:
        GPIO.setup(pins["fan_pwm"], GPIO.OUT)
        fan_pwm = GPIO.PWM(pins["fan_pwm"], 25000)  # 25 kHz
        fan_pwm.start(0)

    return outputs, fan_pwm


def set_output(outputs, name, on: bool):
    pin, active_low = outputs[name]
    if active_low:
        GPIO.output(pin, GPIO.LOW if on else GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.HIGH if on else GPIO.LOW)


def pulse(outputs, name, seconds):
    set_output(outputs, name, True)
    time.sleep(seconds)
    set_output(outputs, name, False)
