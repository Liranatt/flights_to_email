# In CONFIG.py
import os

# SerpAPI config
# Reads the API_KEY from the environment variables (or GitHub Secrets)
API_KEY = os.environ.get('API_KEY')
DEPARTURE_ID = "TLV"
OUTBOUND_DATE = "2026-03-19"
RETURN_DATE = "2026-03-22"

# Email Config
# Reads email credentials from the environment variables
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
SMTP_SERVER = "smtp.gmail.com"

SMTP_PORT = 587
