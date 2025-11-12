
---

### `docs/roadmap.md`
```markdown
# Roadmap

## Fase 1 (listo/en progreso)
- [x] Control de bomba + 2 válvulas.
- [x] Sensores básicos (suelo DO, tanque DO, luz DO).
- [x] DHT11 (temp/humedad).
- [x] Ultrasónico con divisor.
- [x] Ventilador PWM.
- [x] LCD 16×2 con estado en tiempo real.
- [x] Script de **bootstrap** y servicio systemd.

## Fase 2 (próximos hits)
- [ ] **API local** (`web/api/`) con Flask/FastAPI: lectura de estado y endpoints de riego manual.
- [ ] **Cliente web** (`web/client/` – same.dev/Netlify) para control remoto básico.
- [ ] **Logs** en `~/sistema_riego/logs/` y rotación.
- [ ] **Alertas** (bajo nivel de tanque, fallo de sensor) por Telegram/Email.
- [ ] **Calibración guiada** para DO, umbrales y horarios desde la web.
- [ ] **Perfil de planta** (orégano, sábila, vicks, graptopetalum) con presets.
- [ ] **Watchdog** + auto-restart del servicio.

## Fase 3 (hardening)
- [ ] Caja impresa 3D y bornera segura para 12 V.  
- [ ] Placa perma-proto o PCB.  
- [ ] Métricas Prometheus / panel Grafana.  
- [ ] OTA simple (pull de Git + restart sin SSH).

