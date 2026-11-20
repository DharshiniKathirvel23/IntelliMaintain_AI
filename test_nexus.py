
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("NEXUS_API_KEY"),
    base_url=os.getenv("NEXUS_API_BASE_URL", "").rstrip("/") + "/v1"
)

try:
    response = client.chat.completions.create(
       model="nova-micro",
        messages=[
            {
                "role": "user",
                "content": "Explain excessive vibration in an industrial motor in three sentences."
            }
        ]
    )

    print("\nNEXUS AI RESPONSE:\n")
    print(response.choices[0].message.content)

except Exception as error:
    print("\nMODEL TEST FAILED:")
    print(error)
