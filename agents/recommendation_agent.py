
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("NEXUS_API_KEY"),
    base_url=os.getenv("NEXUS_API_BASE_URL", "").rstrip("/") + "/v1"
)


def generate_maintenance_plan(fault_analysis):

    prompt = f"""
You are an industrial maintenance recommendation agent.

Based on the following fault investigation, prepare a
structured maintenance action plan.

FAULT INVESTIGATION:
{fault_analysis}

Include:

1. Immediate Actions
2. Recommended Inspection
3. Corrective Maintenance Actions
4. Preventive Maintenance
5. Required Tools
6. Safety Precautions

Important:
- Do not claim that a possible fault is confirmed.
- Do not invent machine-specific specifications.
- Refer to manufacturer instructions where specifications are required.
- Clearly identify actions that require a qualified technician.
- Prioritize machine isolation and safety before inspection.
"""

    response = client.chat.completions.create(
        model="nova-micro",
        messages=[
            {
                "role": "system",
                "content": "You are an industrial maintenance planning assistant."
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

    sample_analysis = """
    Possible causes of excessive vibration:
    1. Bearing wear
    2. Shaft misalignment
    3. Loose mounting components
    4. Rotor imbalance

    These are possible causes, not confirmed faults.
    """

    plan = generate_maintenance_plan(sample_analysis)

    print("\nMAINTENANCE RECOMMENDATION AGENT")
    print("-" * 45)
    print(plan)
