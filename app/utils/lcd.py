import time
import RPi.GPIO as GPIO


class Lcd16x2:
    """Driver mínimo para HD44780 en modo 4-bit."""
    def __init__(self, rs, e, d4, d5, d6, d7, cols=16, rows=2):
        self.rs, self.e = rs, e
        self.d = [d4, d5, d6, d7]
        self.cols, self.rows = cols, rows

        GPIO.setup(self.rs, GPIO.OUT)
        GPIO.setup(self.e,  GPIO.OUT)
        for p in self.d:
            GPIO.setup(p, GPIO.OUT)

        self._init()

    # --- bajo nivel ---
    def _pulse(self):
        GPIO.output(self.e, False)
        time.sleep(0.0005)
        GPIO.output(self.e, True)
        time.sleep(0.0005)
        GPIO.output(self.e, False)
        time.sleep(0.0005)

    def _nibble(self, val):
        for i, p in enumerate(self.d):
            GPIO.output(p, bool(val & (1 << (3 - i))))
        self._pulse()

    def _byte(self, val, rs=False):
        GPIO.output(self.rs, rs)
        self._nibble(val >> 4)
        self._nibble(val & 0x0F)
        time.sleep(0.0005)

    def _cmd(self, c): self._byte(c, rs=False)
    def _data(self, c): self._byte(c, rs=True)

    def _init(self):
        time.sleep(0.05)
        for _ in range(3):
            self._nibble(0x03); time.sleep(0.004)
        self._nibble(0x02)             # 4-bit
        self._cmd(0x28)                # 2 líneas, 5x8
        self._cmd(0x0C)                # display on, cursor off
        self._cmd(0x06)                # entry mode
        self.clear()

    # --- alto nivel ---
    def clear(self):
        self._cmd(0x01); time.sleep(0.002)

    def home(self):
        self._cmd(0x02); time.sleep(0.002)

    def set_cursor(self, col, row):
        base = [0x00, 0x40][min(row, 1)]
        self._cmd(0x80 | (base + col))

    def print(self, text, row=0, col=0):
        self.set_cursor(col, row)
        for ch in str(text)[: self.cols - col]:
            self._data(ord(ch))
