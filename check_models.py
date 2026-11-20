
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API credentials from .env
load_dotenv()

api_key = os.getenv("NEXUS_API_KEY")
base_url = os.getenv("NEXUS_API_BASE_URL")

if not api_key or not base_url:
    print("API key or Base URL is missing in .env")
else:
    client = OpenAI(
        api_key=api_key,
        base_url=base_url.rstrip("/") + "/v1"
    )

    try:
        models = client.models.list()

        print("\n========== ENABLED API MODELS ==========\n")

        for model in models.data:
            print("Model ID:", model.id)

        print("\n========================================")

    except Exception as error:
        print("API Error:", error)
