
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("NEXUS_API_KEY"),
    base_url=os.getenv("NEXUS_API_BASE_URL").rstrip("/") + "/v1"
)

try:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input="Industrial motor excessive vibration"
    )

    print("Embedding API: SUCCESS")
    print("Model:", response.model)
    print("Embedding dimensions:", len(response.data[0].embedding))

except Exception as error:
    print("Embedding API: FAILED")
    print(error)
