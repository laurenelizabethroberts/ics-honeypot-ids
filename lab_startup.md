# ICS Honeypot + Suricata Lab Startup Guide

This guide explains how to start the ICS Honeypot + Suricata IDS lab manually. You will use four terminals:

* Terminal 1: Start the Conpot honeypot

* Terminal 2: Run Suricata to monitor traffic

* Terminal 3: Watch live Suricata alerts

* Terminal 4: Simulate an attacker (Nmap Modbus scan)

Step 1: Launch Conpot (ICS Honeypot)

Run Conpot in Docker, exposing Modbus/TCP on port 5020:
sudo docker run --rm -it --name conpot -p 5020:5020 honeynet/conpot:latest
  * Conpot is now listening for Modbus traffic

Step 2: Start Suricata IDS

Run Suricata on the docker0 interface with AF-Packet mode for performance:
sudo suricata -i docker0 -c /etc/suricata/suricata.yaml --af-packet
  * Suricata is now inspecting packets on the honeypot interface
Logs are written to:
/var/log/suricata/eve.json

Step 3: Monitor Alerts in Real Time

Use jq to filter only Suricata alerts from the EVE JSON log:
sudo tail -f /var/log/suricata/eve.json | jq 'select(.event_type=="alert") | {time:.timestamp, src:.src_ip, dst:.dst_ip, sig:.alert.signature}'
You will see JSON format like this:
{
  "time": "2025-10-03T15:02:11.123Z",
  "src": "127.0.0.1",
  "dst": "127.0.0.1",
  "sig": "ICSHONEY: Modbus Write Single Coil (FC=5)"
}

Step 4: Simulate an Attack with Nmap

Use Nmap’s Modbus script to probe the honeypot:
sudo nmap -sT -p 5020 --script modbus-discover 127.0.0.1
  * This traffic should trigger alerts in Terminal 3

# Notes 
If Suricata produces no alerts:
* Make sure your custom rules are loaded (/etc/suricata/rules/custom.modbus.rules).

* Check that you are scanning the right port (5020 in this example).

* Verify you are monitoring the correct interface (docker0 or eth0).

You can stop everything with:
docker stop conpot
pkill suricata

# Barebones Start-up

Terminal 1: sudo docker run --rm -it --name conpot -p 5020:5020 honeynet/conpot:latest

Terminal 2: sudo suricata -i docker0 -c /etc/suricata/suricata.yaml --af-packet

Terminal 3: sudo tail -f /var/log/suricata/eve.json | jq 'select(.event_type=="alert") | {time:.timestamp, src:.src_ip, dst:.dst_ip, sig:.alert.signature}'

Terminal 4: sudo nmap -sT -p 5020 --script modbus-discover 127.0.0.1
