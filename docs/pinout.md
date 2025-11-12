# Pinout del sistema (Raspberry Pi 5 – numeración **BCM**)

> Los números corresponden a **BCM** (no físicos). Todos los GPIO trabajan a **3.3 V**.

| Función                       | GPIO (BCM) | Notas                                                                              |
|------------------------------|------------|------------------------------------------------------------------------------------|
| **Bomba (relé)**             | 17         | Módulo de relés activo en **LOW**.                                                 |
| **Válvula 1 (relé)**         | 22         | Zona 1 (con sensores).                                                             |
| **Válvula 2 (relé)**         | 23         | Zona 2 (programada).                                                               |
| **LED UV (simulado)**        | 18         | Usar resistencia serie (≥220 Ω si lo alimentas desde 5 V por transistor/relé).     |
| **Sensor suelo (DO)**        | 27         | Entrada digital; el comparador del módulo define 0/1.                              |
| **Sensor tanque (DO)**       | 26         | Flotador/llave de nivel (o comparador), activo **alto** = falta de agua (config).  |
| **LDR / luz (DO)**           | 24         | Desde módulo comparador: 1 = poca luz (ajustable con potenciómetro del módulo).    |
| **DHT11 (DATA)**             | 5          | Alimentado a **3.3 V**. Pull-up ya incluido en la placa típica.                    |
| **Ventilador PWM**           | 6          | Salida PWM (25 kHz) hacia MOSFET/ULN2003.                                          |
| **Ultrasónico TRIG**         | 12         | Señal de disparo (3.3 V).                                                          |
| **Ultrasónico ECHO**         | 16         | **Debe entrar a 3.3 V** (poner divisor si el módulo entrega 5 V).                  |
| **LCD RS**                   | 25         |                                                                                     |
| **LCD E**                    | 19         |                                                                                     |
| **LCD D4**                   | 4          |                                                                                     |
| **LCD D5**                   | 13         |                                                                                     |
| **LCD D6**                   | 20         |                                                                                     |
| **LCD D7**                   | 21         |                                                                                     |
| 5 V (alimentación relés)     | —          | Rail superior/bus de 5 V en protoboard.                                            |
| 3.3 V (sensores lógicos)     | —          | Rail inferior/bus de 3.3 V en protoboard.                                          |
| GND (masa común)             | —          | **Una sola masa común** para Pi, relés, sensores, bomba/12 V (comparten GND).      |

> La tabla está alineada con `app/config.yaml`. Si cambias pines ahí, actualiza este documento.
