# API local del sistema de riego (borrador)

_Base URL (Pi):_ `http://<IP_DE_TU_PI>:8080`

Autenticación: **sin auth** en LAN (añadiremos token después).
Formato: `application/json` UTF-8.

---

## Recursos

### 1) Estado general
**GET** `/status`
- **200**:
```json
{
  "uptime_s": 12345,
  "version": "0.1.0",
  "zones": {
    "1": {"pump": false, "valve": false, "mode": "sensors"},
    "2": {"pump": false, "valve": false, "mode": "schedule"}
  },
  "tank": {"ok": true, "distance_cm": 23.4, "low": false}
}
