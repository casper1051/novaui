#!/bin/bash

# Constants
DEVICE="wlan0"
UUID=$(uuidgen)


SSID=$(/home/kipr/wombat-os/flashFiles/wallaby_get_serial.sh)-wombat
PASSWORD=$(/home/kipr/wombat-os/flashFiles/wallaby_get_id.sh)
RASPBERRY_TYPE="3B+"  #Hmm... Pi 5? Maybe? (if you get my reference)

# Find the matching NM connection by SSID
CON_NAME=$(nmcli -g NAME connection show | grep -F "$SSID")

if [ -z "$CON_NAME" ]; then
  echo "Connection '$SSID' not found."
  exit 1
fi

# Attempt to read the stored password (WPA-PSK normally)
PASSWORD=$(nmcli -s -g 802-11-wireless-security.psk connection show "$CON_NAME")

if [ -n "$PASSWORD" ]; then
  echo "$PASSWORD"
else
  echo "Password for $SSID not found or not stored in plaintext."
fi

# Band and channel
if [[ "$RASPBERRY_TYPE" == "3B+" ]]; then
  BAND="a"
  CHANNEL="36"
else
  BAND="bg"
  CHANNEL="1"
fi

# Create AP
nmcli connection add type wifi ifname "$DEVICE" con-name "$SSID" autoconnect no \
  ssid "$SSID"

nmcli connection modify "$SSID" \
  802-11-wireless.mode ap \
  802-11-wireless.band "$BAND" \
  802-11-wireless.channel "$CHANNEL" \
  802-11-wireless-security.key-mgmt wpa-psk \
  802-11-wireless-security.psk "$PASSWORD" \
  ipv4.method shared \
  ipv6.method ignore

# Optional: Assign static IP (like in the botui)
nmcli connection modify "$SSID" ipv4.addresses 192.168.125.1/24

# Start the AP
nmcli connection up "$SSID"
