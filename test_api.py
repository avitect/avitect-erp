#!/usr/bin/env python3
import requests
import sys
import json

BASE = "http://localhost:8000"
EMAIL = "bene@avitect.de"
PASSWORD = "DeinPasswort123"

def pretty(resp):
    try:
        print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    except:
        print(resp.text)

def main():
    # 0) Authenticate
    print("🔑 Fetching JWT token…")
    r = requests.post(
        f"{BASE}/auth/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": EMAIL, "password": PASSWORD},
    )
    r.raise_for_status()
    token = r.json().get("access_token")
    print("✅ Token:", token, "\n")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # 1) Create System
    print("1) Creating System…")
    r = requests.post(f"{BASE}/systems/", headers=headers, json={"object_id": 1, "name": "MultiRoom EG"})
    r.raise_for_status()
    pretty(r)
    print()

    # 2) Create Device
    print("2) Creating Device…")
    r = requests.post(f"{BASE}/devices/", headers=headers, json={
        "system_id": 1, "name": "Sonos Amp 1", "device_type": "Sonos Amp", "object_id": 1
    })
    r.raise_for_status()
    pretty(r)
    print()

    # 3) Create Ports
    print("3) Creating Ports…")
    ports = [
        {"device_id": 1, "name": "HDMI1", "direction": "output", "connectivity": "wired", "connector_type": "HDMI-Stecker", "signal_type": "Video"},
        {"device_id": 1, "name": "IR-In",  "direction": "input",  "connectivity": "wired", "connector_type": "IR-Diode",  "signal_type": "Infrarot"},
    ]
    for p in ports:
        r = requests.post(f"{BASE}/ports/", headers=headers, json=p)
        r.raise_for_status()
        pretty(r)
    print()

    # 4) Create Connection
    print("4) Creating Connection…")
    conn = {
        "from_device_id": 1, "from_port_id": 1,
        "to_device_id":   1, "to_port_id":   2,
        "cable_type": "Standard HDMI", "cable_length": 3.5
    }
    r = requests.post(f"{BASE}/connections/", headers=headers, json=conn)
    r.raise_for_status()
    pretty(r)
    print()

    # 5) List all
    for name, endpoint in [("Systems", "systems"), ("Devices", "devices"), ("Ports", "ports"), ("Connections", "connections")]:
        print(f"{name}:")
        r = requests.get(f"{BASE}/{endpoint}/", headers=headers)
        r.raise_for_status()
        pretty(r)
        print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)
