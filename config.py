import os
from dotenv import load_dotenv

load_dotenv()

NEXUS_API_KEY = os.getenv("NEXUS_API_KEY")

if not NEXUS_API_KEY:
    raise ValueError("Nexus API key not found!")