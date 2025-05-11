#!/usr/bin/env bash
set -euo pipefail

BASE="http://localhost:8000"
EMAIL="bene@avitect.de"
PASSWORD="DeinPasswort123"

echo "🔑 Fetching JWT token…"
TOKEN=$(curl -sSL -X POST "$BASE/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=$EMAIL&password=$PASSWORD" \
  | jq -r .access_token)
echo "✅ Token: $TOKEN"
AUTH="Authorization: Bearer $TOKEN"

echo -e "\n1) Creating System…"
SYS_JSON=$(curl -sSL -X POST "$BASE/systems/" \
    -H "$AUTH" \
    -H "Content-Type: application/json" \
    -d '{"object_id":1,"name":"MultiRoom EG"}')
echo "$SYS_JSON" | jq .
SYS_ID=$(echo "$SYS_JSON" | jq -r .id)

echo -e "\n2) Creating Device…"
DEV_JSON=$(curl -sSL -X POST "$BASE/devices/" \
    -H "$AUTH" \
    -H "Content-Type: application/json" \
    -d '{
      "system_id":'"$SYS_ID"',
      "name":"Sonos Amp 1",
      "device_type":"Sonos Amp",
      "object_id":1
    }')
echo "$DEV_JSON" | jq .
DEV_ID=$(echo "$DEV_JSON" | jq -r .id)

echo -e "\n3) Creating Ports…"
# Output-Port
P1_JSON=$(curl -sSL -X POST "$BASE/ports/" \
    -H "$AUTH" \
    -H "Content-Type: application/json" \
    -d '{
      "device_id":'"$DEV_ID"',
      "name":"HDMI1",
      "direction":"output",
      "connectivity":"wired",
      "connector_type":"HDMI-Stecker",
      "signal_type":"Video"
    }')
echo "$P1_JSON" | jq .
P1_ID=$(echo "$P1_JSON" | jq -r .id)

# Input-Port
P2_JSON=$(curl -sSL -X POST "$BASE/ports/" \
    -H "$AUTH" \
    -H "Content-Type: application/json" \
    -d '{
      "device_id":'"$DEV_ID"',
      "name":"IR-In",
      "direction":"input",
      "connectivity":"wired",
      "connector_type":"IR-Diode",
      "signal_type":"Infrarot"
    }')
echo "$P2_JSON" | jq .
P2_ID=$(echo "$P2_JSON" | jq -r .id)

echo -e "\n4) Creating Connection…"
CONN_JSON=$(curl -sSL -X POST "$BASE/connections/" \
    -H "$AUTH" \
    -H "Content-Type: application/json" \
    -d '{
      "from_device_id":'"$DEV_ID"',
      "from_port_id":'"$P1_ID"',
      "to_device_id":'"$DEV_ID"',
      "to_port_id":'"$P2_ID"',
      "cable_type":"Standard HDMI",
      "cable_length":3.5
    }')
echo "$CONN_JSON" | jq .
CONN_ID=$(echo "$CONN_JSON" | jq -r .id)

echo -e "\n5) Listing All…"
echo "→ Systems:"  
curl -sSL "$BASE/systems/" -H "$AUTH" | jq .

echo "→ Devices:"  
curl -sSL "$BASE/devices/" -H "$AUTH" | jq .

echo "→ Ports:"  
curl -sSL "$BASE/ports/" -H "$AUTH" | jq .

echo "→ Connections:"  
curl -sSL "$BASE/connections/" -H "$AUTH" | jq .
