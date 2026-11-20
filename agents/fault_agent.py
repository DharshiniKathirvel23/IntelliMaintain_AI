
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("NEXUS_API_KEY"),
    base_url=os.getenv("NEXUS_API_BASE_URL", "").rstrip("/") + "/v1"
)


def investigate_fault(question, technical_context):

    prompt = f"""
You are an industrial maintenance fault investigation agent.

Analyze the machine problem using the supplied technical information.

USER QUESTION:
{question}

TECHNICAL INFORMATION:
{technical_context}

Your tasks:
1. Identify possible causes of the fault.
2. Explain why each cause may be responsible.
3. Identify relevant evidence from the technical information.
4. Suggest safe inspection steps.

Important rules:
- Do not invent technical evidence.
- Clearly distinguish possible causes from confirmed faults.
- If the technical information is insufficient, say so.
- Do not recommend unsafe actions.
"""

    response = client.chat.completions.create(
        model="nova-micro",
        messages=[
            {
                "role": "system",
                "content": "You are a careful industrial maintenance investigation assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    question = "Why is machine M101 experiencing excessive vibration?"

    technical_context = """
    Sample technical information:
    Excessive vibration may be associated with bearing wear,
    shaft misalignment, loose mounting components or imbalance.
    """

    result = investigate_fault(question, technical_context)

    print("\nFAULT INVESTIGATION AGENT")
    print("-" * 40)
    print(result)
