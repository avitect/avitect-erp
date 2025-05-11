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
curl -s -X POST "$BASE/systems/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"object_id":1,"name":"MultiRoom EG"}' \
| jq .

echo -e "\n2) Gerät anlegen…"
curl -s -X POST "$BASE/devices/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"system_id":1,"name":"Sonos Amp 1","device_type":"Sonos Amp","object_id":1}' \
| jq .

echo -e "\n3) Ports anlegen…"
curl -s -X POST "$BASE/ports/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"device_id":1,"name":"HDMI1","direction":"output","connectivity":"wired","connector_type":"HDMI-Stecker","signal_type":"Video"}' \
| jq .
curl -s -X POST "$BASE/ports/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"device_id":1,"name":"IR-In","direction":"input","connectivity":"wired","connector_type":"IR-Diode","signal_type":"Infrarot"}' \
| jq .

echo -e "\n4) Connection anlegen…"
curl -s -X POST "$BASE/connections/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"from_device_id":1,"from_port_id":1,"to_device_id":1,"to_port_id":2,"cable_type":"Standard HDMI","cable_length":3.5}' \
| jq .

echo -e "\n5) Alle Daten listen…"
echo " Systems:";     curl -s "$BASE/systems/"      -H "Authorization: Bearer $TOKEN" | jq .
echo " Devices:";     curl -s "$BASE/devices/"      -H "Authorization: Bearer $TOKEN" | jq .
echo " Ports:";       curl -s "$BASE/ports/"        -H "Authorization: Bearer $TOKEN" | jq .
echo " Connections:"; curl -s "$BASE/connections/"  -H "Authorization: Bearer $TOKEN" | jq .
