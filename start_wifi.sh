#!/bin/bash

set -e

# Constants
DEVICE="wlan0"

# Get SSID and PASSWORD from your scripts
SSID="$(/home/kipr/wombat-os/flashFiles/wallaby_get_serial.sh)-wombat"
PASSWORD="$(/home/kipr/wombat-os/flashFiles/wallaby_get_id.sh)"

RASPBERRY_TYPE="3B+"  # For band/channel decision

# Disconnect any current connection on wlan0
echo "Disconnecting any current Wi-Fi connections on $DEVICE..."
nmcli device disconnect "$DEVICE" || true

# Remove any existing connection with same SSID to avoid duplicates
EXISTING_AP=$(nmcli -t -f NAME connection show | grep -Fx "$SSID" || true)
if [ -n "$EXISTING_AP" ]; then
  echo "Deleting existing connection $SSID to avoid conflicts..."
  nmcli connection delete "$SSID"
fi

# Determine band and channel
if [[ "$RASPBERRY_TYPE" == "3B+" ]]; then
  BAND="a"
  CHANNEL="36"
else
  BAND="bg"
  CHANNEL="1"
fi

echo "Creating AP connection with SSID: $SSID, Band: $BAND, Channel: $CHANNEL"

# Create new AP connection
nmcli connection add type wifi ifname "$DEVICE" con-name "$SSID" autoconnect no ssid "$SSID"

nmcli connection modify "$SSID" \
  802-11-wireless.mode ap \
  802-11-wireless.band "$BAND" \
  802-11-wireless.channel "$CHANNEL" \
  802-11-wireless-security.key-mgmt wpa-psk \
  802-11-wireless-security.psk "$PASSWORD" \
  ipv4.method shared \
  ipv6.method ignore \
  ipv4.addresses 192.168.125.1/24

# Bring up the AP
nmcli connection up "$SSID"
