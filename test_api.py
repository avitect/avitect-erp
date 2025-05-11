import os

# Generate a Python script for testing the API
script_content = """#!/usr/bin/env python3
import requests
import json

BASE = "http://localhost:8000"
EMAIL = "bene@avitect.de"
PASSWORD = "DeinPasswort123"

def pretty_print(title, data):
    print(f"\\n{title}")
    print(json.dumps(data, indent=2, ensure_ascii=False))

# 1. Get JWT token
resp = requests.post(
    f"{BASE}/auth/login",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={"username": EMAIL, "password": PASSWORD}
)
resp.raise_for_status()
token = resp.json()["access_token"]
print("✅ Token erhalten:", token)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 2. Create a system
resp = requests.post(
    f"{BASE}/systems/",
    headers=headers,
    json={"object_id": 1, "name": "MultiRoom EG"}
)
pretty_print("1) System anlegen…", resp.json())

# 3. Create a device
resp = requests.post(
    f"{BASE}/devices/",
    headers=headers,
    json={"system_id": 1, "name": "Sonos Amp 1", "device_type": "Sonos Amp", "object_id": 1}
)
pretty_print("2) Gerät anlegen…", resp.json())

# 4. Create ports
ports = [
    {"device_id": 1, "name": "HDMI1", "direction": "output", "connectivity": "wired", "connector_type": "HDMI-Stecker", "signal_type": "Video"},
    {"device_id": 1, "name": "IR-In", "direction": "input", "connectivity": "wired", "connector_type": "IR-Diode", "signal_type": "Infrarot"}
]
for idx, p in enumerate(ports, start=3):
    resp = requests.post(f"{BASE}/ports/", headers=headers, json=p)
    pretty_print(f"{idx}) Port anlegen…", resp.json())

# 5. Create a connection
resp = requests.post(
    f"{BASE}/connections/",
    headers=headers,
    json={"from_device_id": 1, "from_port_id": 1, "to_device_id": 1, "to_port_id": 2, "cable_type": "Standard HDMI", "cable_length": 3.5}
)
pretty_print("5) Connection anlegen…", resp.json())

# 6. List all data
for name, endpoint in [("Systems", "systems"), ("Devices", "devices"), ("Ports", "ports"), ("Connections", "connections")]:
    resp = requests.get(f"{BASE}/{endpoint}/", headers=headers)
    pretty_print(f"{name}:", resp.json())
"""

# Save the script to a file
script_path = "/mnt/data/test_api.py"
with open(script_path, "w") as f:
    f.write(script_content)

# Make it executable
os.chmod(script_path, 0o755)

script_path
