# ICS Honeypot Incident Report

# Summary

Suricata detected Modbus probe traffic directed at the Conpot ICS honeypot (port 5020/tcp).
The activity was identified by custom Modbus detection rules (rules/custom.modbus.rules).
Evidence is included in pcaps/ and Suricata EVE JSON logs.

# Indicators of Compromise

| Indicator | Type       | Description                                  |
| --------- | ---------- | -------------------------------------------- |
| 127.0.0.1 | IP Address | Source of Modbus probe (test attacker host)  |
| 5020/tcp  | Port       | Destination Modbus honeypot service          |
| FC=43     | Modbus     | Function code: Device Identification request |

# Timeline of Events

| Time (UTC)       | Event Description                                                |
| ---------------- | ---------------------------------------------------------------- |
| 2025-10-03 15:00 | Conpot honeypot started on port 5020                             |
| 2025-10-03 15:02 | Suricata alert: "ICSHONEY: Modbus Device Identification (FC=43)" |
| 2025-10-03 15:03 | Nmap `modbus-discover` script run from attacker system           |
| 2025-10-03 15:04 | Alerts confirmed in `/var/log/suricata/eve.json`                 |

# Analysis

* The traffic originated from a host running nmap against the honeypot.

* The Modbus function code 43 (Device Identification) is often used for reconnaissance, allowing attackers to fingerprint ICS devices.

* Suricata correctly parsed the Modbus application-layer protocol and triggered on custom rules.

* The honeypot was not affected; activity was safely contained in a controlled lab environment.

# Evidence

* Suricata rule hit:

alert modbus any any -> any 502 (
  msg:"ICSHONEY: Modbus Device Identification (FC=43)";
  app-layer-protocol:modbus;
  flow:established,to_server;
  modbus.func_code:43;
  sid:1000004; rev:1;
)


* Suricata EVE log extract:

{
  "timestamp": "2025-10-03T15:02:11.123Z",
  "src_ip": "127.0.0.1",
  "dest_ip": "127.0.0.1",
  "alert": {
    "signature": "ICSHONEY: Modbus Device Identification (FC=43)",
    "category": "Potential Modbus Reconnaissance"
  }
}


* PCAP sample: stored under pcaps/incident1.pcap

# Recommendations

* Continue to expand Suricata ruleset to include write coil/register commands, which represent higher-impact attacks.

* Deploy log forwarding into ELK/Grafana for correlation and visualization.

* Create detection use-cases for broadcast Modbus traffic (unit_id=0) to detect worm-like behavior.

* Document lab exercises and share as part of threat-hunting portfolio.


Suricata detected Modbus probe traffic to the Conpot honeypot (port 5020).
See `rules/custom-ics.rules` and `pcaps/` for evidence.
