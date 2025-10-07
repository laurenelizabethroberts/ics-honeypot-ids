# Methodology
1. Start services: `make up`
2. Generate traffic: `make trigger` (Read Coils, bulk Read Holding Registers)
3. Observe alerts: `make alerts` (tail `suricata/log/eve.json`)
4. Save excerpts: copy alert JSON lines and `fast.log` entries into `report/evidence/`
5. Snapshot configs: copy current `docker-compose.yml` and `custom.modbus.rules` into `report/artifacts/`
6. Record commit hash for reproducibility: `git rev-parse --short HEAD`
