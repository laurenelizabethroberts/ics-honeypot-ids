# ICS Honeypot with Suricata IDS

This project demonstrates an **ICS (Industrial Control Systems) honeypot** using Conpot alongside **Suricata IDS** to detect malicious or unauthorized Modbus traffic.  
It is designed to showcase practical skills in threat detection, packet analysis, and incident response.

## Quickstart
1. Start Conpot (example):
   sudo docker run --rm -it --name conpot -p 5020:5020 honeynet/conpot:latest

2. Run Suricata on the Docker bridge (example):
   sudo suricata -i docker0 -c /etc/suricata/suricata.yaml --af-packet

3. Trigger a Modbus probe (local test):
   sudo nmap -sT -p 5020 --script modbus-discover 127.0.0.1

Alerts: /var/log/suricata/eve.json  
PCAPs: pcaps/modbus_scan.pcap  
Report: incident.md
