
---

## 2) One-page executive summary

```markdown
# Executive Summary — ICS Modbus Detection Lab
**Date:** 2025-10-07 • **Author:** Lauren Roberts

**What I did:** Built a minimal ICS traffic lab (Conpot) and validated Suricata detections for Modbus reads using custom rules.

**Why it matters:** Shows capability to set up an ICS-aware IDS, generate controlled protocol traffic, and produce analyst-ready evidence and recommendations.

**Key outcomes:**
- Confirmed alerts for:
  - Read Coils (FC=1)
  - Bulk Read Holding Registers (>64)
- Captured structured EVE JSON + fast.log lines with clear signatures.

**Risk & impact (lab context):**
- Reconnaissance-style reads are medium-severity in production ICS as they can reveal process state. Impact depends on asset criticality and access scope.

**Recommendations (short):**
1. Expand rule coverage (write ops; precise PDU matching).
2. Add dashboards + alert enrichment for triage.
3. Baseline normal Modbus volumes per asset.

**Evidence:**
See `report/evidence/` for trimmed logs and screenshot.
