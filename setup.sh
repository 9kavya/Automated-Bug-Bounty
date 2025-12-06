#!/bin/bash
# Automated Bug Bounty Toolkit Setup
# Owner: Jashu

echo "[*] Updating system..."
sudo apt update -y
sudo apt upgrade -y

echo "[*] Installing required Linux tools..."
sudo apt install -y python3 python3-venv python3-pip subfinder amass httprobe nmap whatweb nuclei ffuf chromium

echo "[*] Creating Python virtual environment..."
python3 -m venv venv

echo "[*] Activating virtual environment and installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

echo "[✓] Setup complete! To use the toolkit, run:"
echo "      source venv/bin/activate"
echo "      TARGET=example.com ./run_all.sh"
