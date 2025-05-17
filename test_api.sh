# scripts/test_api.sh
#!/usr/bin/env bash
set -euo pipefail

BASE="http://localhost:8000"
EMAIL="bene@avitect.de"
PASSWORD="DeinPasswort123"

echo "Fetching JWT token…"
TOKEN=$(curl -sSL -X POST "$BASE/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=$EMAIL&password=$PASSWORD" \
    | jq -r '.access_token')  # Token aus JSON holen :contentReference[oaicite:0]{index=0}
echo "✅ Token: $TOKEN"

echo -e "\n1) Creating System…"
SYS_JSON=$(curl -sSL -X POST "$BASE/systems/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"object_id":1,"name":"MultiRoom EG"}')
echo "$SYS_JSON" | jq .
SYSTEM_ID=$(echo "$SYS_JSON" | jq -r '.id')
echo "→ system_id = $SYSTEM_ID"

echo -e "\n2) Creating Device…"
DEV_JSON=$(curl -sSL -X POST "$BASE/devices/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"system_id\":$SYSTEM_ID,\"name\":\"Sonos Amp 1\",\"device_type\":\"Sonos Amp\",\"object_id\":1}")
echo "$DEV_JSON" | jq .
DEVICE_ID=$(echo "$DEV_JSON" | jq -r '.id')
echo "→ device_id = $DEVICE_ID"

echo -e "\n3) Creating Ports…"
PORT1_JSON=$(curl -sSL -X POST "$BASE/ports/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"device_id\":$DEVICE_ID,\"name\":\"HDMI1\",\"direction\":\"output\",\"connectivity\":\"wired\",\"connector_type\":\"HDMI-Stecker\",\"signal_type\":\"Video\"}")
echo "$PORT1_JSON" | jq .
PORT1_ID=$(echo "$PORT1_JSON" | jq -r '.id')

PORT2_JSON=$(curl -sSL -X POST "$BASE/ports/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"device_id\":$DEVICE_ID,\"name\":\"IR-In\",\"direction\":\"input\",\"connectivity\":\"wired\",\"connector_type\":\"IR-Diode\",\"signal_type\":\"Infrarot\"}")
echo "$PORT2_JSON" | jq .
PORT2_ID=$(echo "$PORT2_JSON" | jq -r '.id')

echo -e "\n4) Creating Connection…"
CONN_JSON=$(curl -sSL -X POST "$BASE/connections/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"from_device_id\":$DEVICE_ID,\"from_port_id\":$PORT1_ID,\"to_device_id\":$DEVICE_ID,\"to_port_id\":$PORT2_ID,\"cable_type\":\"Standard HDMI\",\"cable_length\":3.5}")
echo "$CONN_JSON" | jq .

echo -e "\n5) Listing All Data…"
curl -sSL "$BASE/systems/"      -H "Authorization: Bearer $TOKEN" | jq .
curl -sSL "$BASE/devices/"      -H "Authorization: Bearer $TOKEN" | jq .
curl -sSL "$BASE/ports/"        -H "Authorization: Bearer $TOKEN" | jq .
curl -sSL "$BASE/connections/"  -H "Authorization: Bearer $TOKEN" | jq .
