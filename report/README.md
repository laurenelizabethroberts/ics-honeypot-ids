# Reports — ICS Modbus Detection Lab

This folder contains manager-friendly writeups and analyst evidence for runs of the **Conpot + Suricata** mini-lab. Each report is reproducible and tied to a specific commit.

---

## What lives here
├─ YYYY-MM-DD_title.md # main report(s)

├─ exec_summary.md # optional 1-pager for non-technical readers

├─ methodology.md # optional detailed runbook

├─ evidence/

│ ├─ eve_excerpt.json # trimmed EVE alert(s)

│ ├─ fast_excerpt.log # a few alert lines

│ └─ screenshots/

│ └─ eve-alerts.png # screenshot of alerts

└─ artifacts/

├─ docker-compose.yml # snapshot of what was used for the run

└─ custom.modbus.rules # snapshot of rules used


> **Naming convention:** use `YYYY-MM-DD_short-title.md` (e.g., `2025-10-07_ics-modbus-demo.md`).

---

## How to (re)generate evidence

From the repo root:

```bash
make up
make trigger
# watch alerts in another terminal (Ctrl+C to stop)
make alerts
make down
```

Then collect small excerpts

```bash
# EVE excerpt (no jq required)
grep '"event_type":"alert"' suricata/log/eve.json | head -n 5 > report/evidence/eve_excerpt.json

# fast.log excerpt (if enabled by your Suricata config)
tail -n 5 suricata/log/fast.log > report/evidence/fast_excerpt.log
```

Take a screenshot of alerts and save as:
```bash
report/evidence/screenshots/eve-alerts.png
```

Snapshot the exact configurations you used for the run:
```bash
cp docker-compose.yml report/artifacts/docker-compose.yml
cp suricata/rules/custom.modbus.rules report/artifacts/custom.modbus.rules
```
# Report checklist (QA)
 Report file created with today’s date and short title
 Commit hash included at top of report (git rev-parse --short HEAD)
 EVE + fast excerpts added under report/evidence/
 Screenshot placed in report/evidence/screenshots/
 docker-compose.yml + rules snapshot copied into report/artifacts/
 Recommendations & next steps written (at least 2–3 bullets)
 Sensitive data redacted (no real IPs/secrets)

# Template - new report
copy this into a new file like report/2025-10-07_ics-modbus-demo.md:

```bash
# ICS Modbus Detection Lab — Suricata + Conpot
**Date:** 2025-10-07  
**Author:** Lauren Roberts  
**Commit:** `<short-hash>`  

## Executive Summary
One paragraph: what you built, what you tested, what you proved, outcome in plain English.

## Objectives
- Emulate ICS Modbus traffic safely.
- Validate Suricata parses Modbus and fires custom rules.
- Produce analyst-ready evidence and recommendations.

## Environment
- macOS + Docker Desktop • Containers: Conpot, Suricata, Python (attacker)
- Network: Docker bridge `icynet`
- Artifacts: see `report/artifacts/`

## Method
1. `make up`  → start lab  
2. `make trigger` → send Modbus reads (FC=1, FC=3 bulk)  
3. `make alerts` → observe `suricata/log/eve.json`  
4. Save excerpts & screenshots into `report/evidence/`

## Results (highlights)
- **Alert 1:** MODBUS Read Coils (FC=1) detected — `sid:1000001`  
- **Alert 2:** Bulk Read Holding Registers (>64) detected — `sid:1000002`  

**EVE excerpt:** see `report/evidence/eve_excerpt.json`  
**fast.log excerpt:** see `report/evidence/fast_excerpt.log`  
![Suricata EVE alerts](evidence/screenshots/eve-alerts.png)

## Findings & Recommendations
- Finding: Recon-style reads observed; detections fire as expected.  
- Recs: Expand rule coverage (write ops), enrich alerts, add dashboard panels.

## Limitations
Synthetic lab traffic; rules simplified for clarity (tighten offsets in production).

## Next Steps
Add write-operation tests (FC=5/16), store a PCAP + hash, and publish a short triage ticket sample.
```

# Ethics & scope
This lab is for local, permissioned testing only. Do not scan or interact with systems you do not own or explicitly control.


