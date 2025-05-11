#!/usr/bin/env bash
set -euo pipefail

BASE="http://localhost:8000"
EMAIL="bene@avitect.de"
PASSWORD="DeinPasswort123"

echo "🔑 Hole JWT-Token…"
TOKEN=$(
  curl -sSL -X POST "$BASE/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=$EMAIL&password=$PASSWORD" \
    | jq -r .access_token
)
echo "✅ Token erhalten: $TOKEN"

echo -e "\n1) System anlegen…"
curl -sSL -L -X POST "$BASE/systems/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"object_id":1,"name":"MultiRoom EG"}' \
| jq .

echo -e "\n2) Gerät anlegen…"
curl -sSL -L -X POST "$BASE/devices/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"system_id":1,"name":"Sonos Amp 1","device_type":"Sonos Amp","object_id":1}' \
| jq .

echo -e "\n3) Ports anlegen…"
curl -sSL -L -X POST "$BASE/ports/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"device_id":1,"name":"HDMI1","direction":"output","connectivity":"wired","connector_type":"HDMI-Stecker","signal_type":"Video"}' \
| jq .
curl -sSL -L -X POST "$BASE/ports/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"device_id":1,"name":"IR-In","direction":"input","connectivity":"wired","connector_type":"IR-Diode","signal_type":"Infrarot"}' \
| jq .

echo -e "\n4) Connection anlegen…"
curl -sSL -L -X POST "$BASE/connections/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"from_device_id":1,"from_port_id":1,"to_device_id":1,"to_port_id":2,"cable_type":"Standard HDMI","cable_length":3.5}' \
| jq .

echo -e "\n5) Alle Daten listen…"
echo " Systems:";     curl -sSL -L "$BASE/systems/"      -H "Authorization: Bearer $TOKEN" | jq .
echo " Devices:";     curl -sSL -L "$BASE/devices/"      -H "Authorization: Bearer $TOKEN" | jq .
echo " Ports:";       curl -sSL -L "$BASE/ports/"        -H "Authorization: Bearer $TOKEN" | jq .
echo " Connections:"; curl -sSL -L "$BASE/connections/"  -H "Authorization: Bearer $TOKEN" | jq .
