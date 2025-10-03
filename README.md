# ICS Honeypot with Suricata IDS (Modbus)
![License](https://img.shields.io/github/license/laurenelizabethroberts/ics-honeypot-ids?cacheSeconds=1)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)


An ICS honeypot lab using Conpot monitored by Suricata with custom Modbus rules.
Use it to practice detection engineering for OT/ICS, generate incident reports, and showcase blue-team skills.

* See lab_startup.md to relaunch after reboot.

* See incident.md for a sample investigation report format.

# What You Get

* Conpot simulating ICS services (Modbus/TCP on 502/tcp, plus optional HTTP/SNMP banners).

* Suricata watching the traffic and alerting on Modbus behaviors (read/write coils/registers, device identification, broadcast writes, etc.).

* EVE JSON logs for easy parsing (/var/log/suricata/eve.json) and a crisp workflow to go from alert ➜ artifact ➜ report.

# Architecture

+----------------------------+         +--------------------------+
|        Attacker/Client     |         |        Analyst Host      |
| (modbus-cli, nmap, etc.)   |         |  - Suricata              |
|            |               |         |  - EVE JSON + jq         |
+------------|---------------+         |  - (Optional) Loki/Graf. |
             |                         +-----------|--------------+
             v                                     |
        +-------------------+                      |
        |      Conpot       |  (host network)      |
        |  ICS Honeypot     |<---------------------+
        |  Modbus/TCP :502  |
        +-------------------+

# Quickstart

1) Files to add to repo
Create this structure:
ics-honeypot-ids/
├─ docker-compose.yml

├─ Makefile

├─ suricata/

│  ├─ suricata.yaml            # (optional: minimal edits snippet below)

│  └─ rules/

│     └─ custom.modbus.rules   # provided below

├─ lab_startup.md

├─ incident.md

└─ README.md

2) docker-compose.yaml
Change eth0 to the correct interface for your host.

3) Custom Modbus Rules (suricata/rules/custom.modbus.rules)

#Generic Modbus traffic to the honeypot
alert modbus any any -> any 502 (
  msg:"ICSHONEY: Modbus request to honeypot";
  app-layer-protocol:modbus;
  flow:established,to_server;
  sid:1000001; rev:1;
)

#Write Single Coil (0x05) - Often used to change actuator state
alert modbus any any -> any 502 (
  msg:"ICSHONEY: Modbus Write Single Coil (FC=5)";
  app-layer-protocol:modbus;
  flow:established,to_server;
  modbus.func_code:5;
  sid:1000002; rev:1;
)

#Write Multiple Registers (0x10 / 16) - Could change critical setpoints
alert modbus any any -> any 502 (
  msg:"ICSHONEY: Modbus Write Multiple Registers (FC=16)";
  app-layer-protocol:modbus;
  flow:established,to_server;
  modbus.func_code:16;
  sid:1000003; rev:1;
)

#Read Device Identification (0x2B / 43) - Recon behavior
alert modbus any any -> any 502 (
  msg:"ICSHONEY: Modbus Device Identification (FC=43)";
  app-layer-protocol:modbus;
  flow:established,to_server;
  modbus.func_code:43;
  sid:1000004; rev:1;
)

#Broadcast writes (Unit ID 0) are suspicious on some networks
alert modbus any any -> any 502 (
  msg:"ICSHONEY: Modbus broadcast (unit_id=0)";
  app-layer-protocol:modbus;
  flow:established,to_server;
  modbus.unit_id:0;
  sid:1000005; rev:1;
)

#Abnormally large Modbus payload (simple heuristic)
alert modbus any any -> any 502 (
  msg:"ICSHONEY: Modbus large data payload";
  app-layer-protocol:modbus;
  flow:established,to_server;
  modbus.data_len:>256;
  sid:1000006; rev:1;
)

4. suricata.yaml tweaks
If you mount your own suricata.yaml, ensure EVE JSON is enabled and points to the mounted log path:\
outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: /var/log/suricata/eve.json
      types:
        - alert
        - http
        - flow
        - tls
        - dns
5. Make it Easy
.PHONY: up down logs alerts test clean

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

alerts:
	@echo "Tailing Suricata alerts (eve.json)..."
	@tail -f suricata_logs/eve.json | jq 'select(.event_type=="alert") | {ts:.timestamp,src:.src_ip,dst:.dest_ip,msg:.alert.signature}'

#Simple Modbus probe using Python + pymodbus (requires Python + pip)
test:
	python3 - <<'PY'
from pymodbus.client import ModbusTcpClient
c=ModbusTcpClient("127.0.0.1", port=502)
c.connect()
#Read holding registers (FC=3) - recon
print("Read HR:", c.read_holding_registers(0,2).function_code)
#Write single coil (FC=5) - should trigger alert
print("Write Coil:", c.write_coil(1, True).function_code)
c.close()
PY

clean:
	rm -rf suricata_logs/* conpot_logs/*

# Use It:
1. Start the lab:
make up
2. Generate Traffic
From you analyst box (or same host), run:
make test
or use your own rules:
#nmap modbus probe
nmap -sT -p 502 --script modbus-discover 127.0.0.1
3. Watch Alerts
make alerts
You should see entries like:
{"ts":"2025-10-03T14:10:22.123Z","src":"127.0.0.1","dst":"127.0.0.1","msg":"ICSHONEY: Modbus Write Single Coil (FC=5)"}
4. Stop the Lab:
make down

# Paths and Artifacts
Conpot logs: ./conpot_logs/

Suricata EVE JSON: ./suricata_logs/eve.json

Custom rules: ./suricata/rules/custom.modbus.rules

Use these artifacts in incident.md to write up findings (IOC tables, timelines, PCAP references if you capture).

# Troubleshooting
No alerts?

* Confirm the interface in docker-compose.yml (-i ethX) matches your host NIC.

* Ensure traffic is to port 502/tcp on the host (Conpot uses host network).

* Tail raw EVE to verify events:

tail -f suricata_logs/eve.json


* Port already in use? Something else is on 502/tcp. Stop it or adjust Conpot profile/port.

* jq not found? Install it (apt, brew, choco) or use tail -f without filtering.

# Safety and Ethics
This is a lab honeypot. Keep it isolated (e.g., home lab/VLAN).
Do not expose to the public internet unless you understand the risks and compliance implications.

# Next Steps
* Add Grafana/Loki to visualize Suricata alerts.

* Expand Modbus rules with plant-specific unit IDs/register maps.

* Add PCAP capture (e.g., tcpdump) for packet-level forensics in your incident.md.

# License
MIT.



