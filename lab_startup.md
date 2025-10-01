# ICS Honeypot + Suricata Lab Startup Guide
Terminal 1: sudo docker run --rm -it --name conpot -p 5020:5020 honeynet/conpot:latest
Terminal 2: sudo suricata -i docker0 -c /etc/suricata/suricata.yaml --af-packet
Terminal 3: sudo tail -f /var/log/suricata/eve.json | jq 'select(.event_type=="alert") | {time:.timestamp, src:.src_ip, dst:.dst_ip, sig:.alert.signature}'
Terminal 4: sudo nmap -sT -p 5020 --script modbus-discover 127.0.0.1
