#!/bin/bash
# Email Filter Bot — One-time setup script
# Run this once: bash setup.sh

set -e

echo ""
echo "=================================="
echo "   Email Filter Bot — Setup"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Download it from https://www.python.org/downloads/ then re-run this script."
    exit 1
fi

echo "Python $(python3 --version) found."

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install openpyxl python-dotenv --quiet
echo "Dependencies installed."

# Collect credentials
echo ""
echo "Enter your webmail credentials:"
echo ""

read -p "  Email address : " EMAIL_ADDRESS
read -s -p "  Password      : " EMAIL_PASSWORD
echo ""
read -p "  IMAP host (press Enter to use mail.privateemail.com) : " IMAP_HOST
IMAP_HOST=${IMAP_HOST:-mail.privateemail.com}

# Write .env
cat > .env <<EOF
EMAIL_ADDRESS=${EMAIL_ADDRESS}
EMAIL_PASSWORD=${EMAIL_PASSWORD}
EMAIL_IMAP_HOST=${IMAP_HOST}
EMAIL_IMAP_PORT=993
EOF

echo ""
echo "Testing connection..."

python3 - <<PYEOF
import imaplib, ssl, os
from dotenv import load_dotenv
load_dotenv()
host = os.getenv('EMAIL_IMAP_HOST')
port = int(os.getenv('EMAIL_IMAP_PORT', 993))
addr = os.getenv('EMAIL_ADDRESS')
pwd  = os.getenv('EMAIL_PASSWORD')
try:
    ctx = ssl.create_default_context()
    conn = imaplib.IMAP4_SSL(host, port, ssl_context=ctx)
    conn.login(addr, pwd)
    conn.logout()
    print("SUCCESS: Connected to", host)
except Exception as e:
    print("FAILED:", e)
    print("")
    print("Check your credentials or IMAP host and re-run setup.sh")
    exit(1)
PYEOF

echo ""
echo "=================================="
echo "  Setup complete!"
echo ""
echo "  Run the bot anytime with:"
echo "    python3 email_filter.py"
echo ""
echo "  Options:"
echo "    --since 7       last 7 days only"
echo "    --limit 100     cap at 100 emails"
echo "    --output FILE   custom output filename"
echo "=================================="
echo ""
