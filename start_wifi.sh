#!/bin/bash

# Constants
DEVICE="wlan0"
UUID=$(uuidgen)


SSID="Test"
PASSWORD="password"
RASPBERRY_TYPE="3B+"  # Change to 3B or 3B+ as detected


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

# Optional: Assign static IP (like in C++ code)
nmcli connection modify "$SSID" ipv4.addresses 192.168.125.1/24

# Start the AP
nmcli connection up "$SSID"
