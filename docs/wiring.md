# Guía de cableado (paso a paso)

## 0) Regletas de la protoboard
- **Regleta superior = 5 V**: alimenta **módulo de relés**, sensores de 5 V y actuadores (vía módulos).
- **Regleta inferior = 3.3 V**: alimenta señales lógicas directas a la Pi (DHT11, salidas comparador de sensores, lado ECHO tras divisor, etc.).
- **GND en común**: une GND de Pi, fuente 12 V (bomba/solenoides), módulo de relés y módulos de sensores.

> No cruces 5 V directamente a GPIOs. Todas las entradas a la Pi deben ser **3.3 V**.

---

## 1) Módulo de relés (4 canales, activo LOW)
- **VCC del módulo** → **5 V** (regleta superior).
- **GND del módulo** → **GND común**.
- **IN1** (bomba) → GPIO **17**  
  **IN2** (válvula 1) → GPIO **22**  
  **IN3** (válvula 2) → GPIO **23**  
  (IN4 libre por ahora)
- Lado de **potencia**:
  - Usa **12 V** para **bomba** y **válvulas**.
  - Conexión típica por canal: **COM** a +12 V, **NO** al dispositivo; el otro cable del dispositivo a **GND 12 V**.
  - Revisa polaridad de la bomba y solenoides (son cargas DC).

> Los relés necesitan **diodos flyback** en paralelo a la **bomba** y a **cada válvula** (1N4007): cátodo a +12 V, ánodo a lado que va al relé.

---

## 2) Sensor de suelo (módulo DO)
- Módulo de suelo con comparador:
  - **VCC** → 5 V o 3.3 V (preferible **3.3 V** si el módulo lo permite; si no, **5 V** y la **salida DO** debe estar 3.3 V-tolerante; la mayoría lo es).
  - **GND** → GND.
  - **DO** → GPIO **27**.
- Ajusta el potenciómetro hasta que **DO=1** en seco y **DO=0** con tierra húmeda (o al revés, y ajusta `umbrales.suelo_seco` en `config.yaml`).

---

## 3) Sensor de nivel del tanque (switch / comparador DO)
- **VCC** → 5 V o 3.3 V según módulo.
- **GND** → GND.
- **DO** → GPIO **26**.
- Convención del proyecto: **1 = SIN AGUA**. Si tu hardware da lo contrario, cambia `umbrales.tanque_min` en `config.yaml`.

---

## 4) LDR (módulo comparador, salida DO)
- **VCC** → 5 V.
- **GND** → GND.
- **DO** → GPIO **24**.
- Ajusta el pot para que **DO=1 cuando hay poca luz** (esto casa con `umbrales.luz_min: 1`).

---

## 5) DHT11 (módulo +/-/S)
- Conecta **+ → 3.3 V**, **– → GND**, **S (DATA) → GPIO 5**.
- La placa suele incluir el **pull-up**; si usas un DHT suelto, añade **resistencia 10 kΩ** entre DATA y **3.3 V**.
- Cables **cortos** y separados de los de la bomba/relés; el DHT odia el ruido.

---

## 6) Ultrasónico HC-SR04
- **VCC** → 5 V.
- **GND** → GND.
- **TRIG** → GPIO **12** (directo, 3.3 V es suficiente).
- **ECHO** → **GPIO 16** a través de **divisor resistivo** (si tu módulo entrega 5 V):
  - Usa **5.1 kΩ arriba** (desde ECHO del sensor) y **10 kΩ abajo** (a GND).  
    La tensión en el nodo a GPIO ≈ **3.31 V** (perfecto).
  - Si no tienes 5.1 k, combina **(10 k || 10 k) ≈ 5 k** como “arriba” + **10 k abajo**.

---

## 7) Ventilador (PWM por MOSFET / ULN2003)
- Señal PWM: **GPIO 6**.
- Con **MOSFET canal N**:
  - **Gate** ← GPIO 6 (con **resistencia serie 220–330 Ω** y **pull-down 100 kΩ** a GND).
  - **Drain** → negativo del ventilador.
  - **Source** → GND.
  - Ventilador positivo → +12 V / +5 V (según modelo).
  - **Diodo flyback** 1N4007 en paralelo si es motor DC (cátodo a +V).
- Con **ULN2003**:
  - Entrada 1 ← GPIO 6 (PWM).
  - Salida 1 → negativo del ventilador; positivo a +V.
  - GND del ULN2003 a GND común; **COM** del ULN a +V para el diodo interno.

---

## 8) LED UV simulado
- Si lo manejas **directo desde GPIO 18**:
  - GPIO 18 → **resistencia 220–330 Ω** → ánodo LED → cátodo a **GND**.
  - Mantén la corriente ≤8–10 mA.
- Si necesitas más luminosidad, usa transistor/MOSFET a 5 V y resistencia adecuada (≈220 Ω para LED típico).

---

## 9) LCD 16×2 (HD44780, 4-bit)
- **VCC** → 5 V, **GND** → GND.
- **VO (contraste)** → pot de 10 k entre 5 V y GND; cursor a VO (ajústalo hasta ver caracteres).
- **RS → GPIO 25**, **E → GPIO 19**.
- **D4→GPIO 4**, **D5→GPIO 13**, **D6→GPIO 20**, **D7→GPIO 21**.
- **RW** a GND (escritura).
- Luz de fondo: **A → 5 V** (con resistencia si tu módulo no la trae), **K → GND**.

---

## 10) Fuente y protecciones
- Pi con su **USB-C oficial** o equivalente estable.
- Actuadores a **12 V**/5 V con su **fuente dedicada**; **GND en común** con la Pi.
- Añade **TVS o varistores** si notas picos por la bomba.
- Cables de potencia separados de señales; usa ferritas si hay ruido.

