# Simple Modbus client to generate Suricata alerts against Conpot
# Usage: make trigger

from pymodbus.client import ModbusTcpClient
import time

CONPOT_HOST = "conpot" # service name on docker network
CONPOT_PORT = 502 # internal port (we mapped host 1502 -> container 502)

if __name__ == "__main__":
    print("[*] Connecting to Conpot Modbus TCP at %s:%s" % (CONPOT_HOST, CONPOT_PORT))
    client = ModbusTcpClient(CONPOT_HOST, port=CONPOT_PORT)
    if not client.connect():
        raise SystemExit("[-] Could not connect to Conpot at %s:%s" % (CONPOT_HOST, CONPOT_PORT))

# 1) Read Coils (should trigger Rule 1)
print("[*] Sending Read Coils (fc=1) request...")
rr = client.read_coils(address=0, count=8, unit=1)
print("[+] Read Coils response: ", rr)

time.sleep(0.5)

# 2) Read Holding Registers with a bigger quantity (aim to trigger Rule 2)
print("[*] Sending Read Holding Registers (fc=3) with large quantity...")
rr2 = client.read_holding_registers(address=0, count=65, unit=1)
print("[+] Read Holding Registers response: ", rr2)

client.close()
print("[*] Done. Check suricata/log/eve.json or run `make alerts`.")
