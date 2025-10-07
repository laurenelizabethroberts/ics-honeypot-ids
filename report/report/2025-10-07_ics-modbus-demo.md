# ICS Modbus Detection Lab — Suricata + Conpot
**Date:** 2025-10-07  
**Author:** Lauren Roberts  
**Repo:** https://github.com/laurenelizabethroberts/ics-honeypot-ids  
**Commit:** `<paste short commit hash>`

## Executive Summary
We stood up a minimal ICS detection lab (Conpot + Suricata) and verified custom Modbus detections. Using a scripted Modbus client, we generated benign probe traffic (Read Coils, bulk Read Holding Registers). Suricata triggered alerts as expected and logged structured events in `eve.json`.  
**Outcome:** The rules reliably detect Modbus reconnaissance-style reads; the lab is reproducible with `make up → make trigger → make alerts`.

## Scope & Objectives
- Emulate basic ICS traffic (Modbus/TCP) safely in a containerized lab.
- Validate Suricata can parse Modbus and fire custom rules.
- Produce analyst-ready evidence (EVE JSON, fast.log) and recommendations.

## Environment
- **Host:** macOS (Docker Desktop)
- **Containers:** `honeynet/conpot:latest`, `jasonish/suricata:latest`, `python:3.11-slim`
- **Network:** Docker bridge (`icynet`)
- **Artifacts:** See `report/artifacts/` for the exact `docker-compose.yml` and rules file.

## Method (high level)
1. `make up` — start Conpot (Modbus on 502) and Suricata (monitoring `eth0`).
2. `make trigger` — run a Python script that performs:
   - Read Coils (FC=1)
   - Read Holding Registers (FC=3) with larger quantity
3. `make alerts` — tail `suricata/log/eve.json` to observe alerts.

## Results (highlights)
- Suricata logged Modbus alerts in `eve.json` and `fast.log`:
  - **MODBUS Read Coils to PLC** (reconnaissance-style read)
  - **MODBUS Bulk Read Holding Registers (quantity > 64)** (suspicious large read)

### Sample EVE JSON (trimmed)
```json
{
  "event_type": "alert",
  "app_proto": "modbus",
  "alert": {
    "signature_id": 1000001,
    "signature": "MODBUS Read Coils to PLC",
    "severity": 2
  },
  "dest_port": 502
}
```
## Sample fast.log line

10/07/25-15:43:12.123456  [**] [1:1000001:1] MODBUS Read Coils to PLC [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 172.20.0.5:51734 -> 172.20.0.4:502

Full excerpts: report/evidence/eve_excerpt.json, report/evidence/fast_excerpt.log.
Screenshot: report/evidence/screenshots/eve-alerts.png.

## Findings
| ID  | Finding                                              | Evidence                | Severity | Likelihood | Notes                                                    |
| --- | ---------------------------------------------------- | ----------------------- | -------- | ---------- | -------------------------------------------------------- |
| F-1 | Modbus Read Coils detected (function code 1)         | EVE alert `sid:1000001` | Medium   | Medium     | Typical recon read against PLC coils.                    |
| F-2 | Bulk Read Holding Registers detected (quantity > 64) | EVE alert `sid:1000002` | Medium   | Medium     | Large data pulls may indicate aggressive reconnaissance. |

## Recommendations
Tune & expand rules: Add more Modbus function code coverage (e.g., write operations) and precise PDU offset checks.

Alert enrichment: Include container/host labels and user-friendly signatures (e.g., “Read Coils (FC=1) from attacker container”).

Dashboards: Add a simple dashboard panel (events over time, top source IPs).

Production note: In real ICS, pair network detections with asset baselines and strict change control to reduce false positives.

## Limitations
Lab traffic is synthetic and safe by design; results demonstrate detection mechanics rather than real adversary behavior.

The “bulk read” rule is intentionally simple; real environments should use field-accurate byte offsets or community rule sets.

## Next Steps
Add write-operation rules (e.g., Write Single Coil FC=5) and test cases.

Generate a small PCAP and store in /pcaps/ with a hash.

Export a short ticket (triage notes) to mimic SOC workflow.

## Appendix
report/artifacts/docker-compose.yml — compose snapshot used.

report/artifacts/custom.modbus.rules — rules snapshot used.

report/methodology.md — detailed runbook (optional).
