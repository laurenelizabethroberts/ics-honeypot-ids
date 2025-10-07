from pymodbus.client import ModbusTcpClient
import time

CONPOT_HOST = "conpot"
CONPOT_PORT = 502

if __name__ == "__main__":
    print(f"[*] Connecting to Conpot Modbus TCP at {CONPOT_HOST}:{CONPOT_PORT}")
    client = ModbusTcpClient(CONPOT_HOST, port=CONPOT_PORT)
    if not client.connect():
        raise SystemExit(f"[-] Could not connect to Conpot at {CONPOT_HOST}:{CONPOT_PORT}")

    print("[*] Sending Read Coils (fc=1) request...")
    rr = client.read_coils(address=0, count=8, unit=1)
    print("[+] Read Coils response:", rr)

    time.sleep(0.5)

    print("[*] Sending Read Holding Registers (fc=3) with large quantity...")
    rr2 = client.read_holding_registers(address=0, count=65, unit=1)
    print("[+] Read Holding Registers response:", rr2)

    client.close()
    print("[*] Done. Check suricata/log/eve.json or run `make alerts`.")
