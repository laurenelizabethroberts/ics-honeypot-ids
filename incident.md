# ICS Honeypot Incident Report

**Date/Time (UTC):** 2025-10-01T12:10:31  
**Source IP:** 172.17.0.1  
**Destination IP:** 172.17.0.2  
**Alert Signature:** ICS: TCP to Modbus port (5020)

## Description
Suricata detected Modbus traffic directed at the honeypot (Conpot) running on port 5020.  
The request originated from the host (172.17.0.1) probing the honeypot container (172.17.0.2).  

This indicates reconnaissance or probing activity targeting Modbus/TCP services.  

## Evidence
- **Suricata alert:**  

