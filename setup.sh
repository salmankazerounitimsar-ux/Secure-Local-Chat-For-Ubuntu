#!/bin/bash

# Clear the screen
clear

echo "=========================================="
echo "    SECURE NODE CHAT INSTALLER"
echo "=========================================="
echo ""

# Update system and install Python pip
echo "[1/3] Updating system packages..."
sudo apt-get update -y > /dev/null

echo "[2/3] Installing Python3 and Pip..."
sudo apt-get install python3 python3-pip -y > /dev/null

# Install Flask
echo "[3/3] Installing Flask library..."
sudo apt install python3-flask -y > /dev/null

echo ""
echo "✅ SETUP COMPLETE!"
echo "------------------------------------------"
echo "To start your chat, use this command format:"
echo "python3 app.py <user> <pass> <secret-url>"
echo ""
echo "Example:"
echo "python3 app.py root 8878Sl8878@S my-secret-room"
echo "------------------------------------------"