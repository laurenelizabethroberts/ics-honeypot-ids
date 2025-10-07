.PHONY: up down logs alerts trigger clean

up:
    docker compose up -d

down:
    docker compose down

logs:
    docker compose logs -f --tail=200

alerts:
    @echo "Tailing Suricata EVE JSON... (Ctrl+C to stop)"
    tail -f suricata/log/eve.json

trigger:
    # Install deps (first run caches in attacker container)
    docker compose exec attacker pip install --quiet pymodbus==3.6.6
    # Run the Modbus probe against Conpot on port 502 inside the icynet
    docker compose exec attacker python /app/trigger_modbus.py

clean:
    rm -rf suricata/log/* || true
