import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Store credentials securely
KITE_USERNAME = os.getenv("KITE_USERNAME")
KITE_PASSWORD = os.getenv("KITE_PASSWORD")
KITE_TOTP_KEY = os.getenv("KITE_TOTP_KEY")
