import os
import json
from openai import OpenAI

# Initialize the secure production-ready gateway pipeline client wrapper
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")  # Dynamically loaded via Cloud Environment configurations
)

def generate_tasks(document_text, dynamic_team=None):
    # Fallback to defaults if list context fails to resolve
    if not dynamic_team:
        dynamic_team = ["Sanju", "Joanna", "Sahana", "Pradeep", "Rakshanaa", "Parkavi"]
        
    # Convert team list cleanly into a formatted string block for the AI model's prompt instructions
    team_prompt_string = "\n".join([f"- {name}" for name in dynamic_team])

    prompt = f"""
You are acting as a Software Project Manager.

Distribute tasks fairly across the following team members:
{team_prompt_string}

Rules:
1. Every single task must be assigned to one of the provided team members.
2. Balance the workload evenly across everyone listed.
3. Do not assign more than two consecutive tasks to the same member.
4. If multiple people are suitable, choose the person with the fewest assigned tasks.
5. At the end, every member should have a similar number of tasks whenever possible.

IMPORTANT RULES
Every task MUST contain ALL FIVE fields.
task
priority
description
assigned_user
time_period

Never omit any field. Never leave any field blank.
time_period must be one of: 1 Day, 2 Days, 3 Days, 5 Days, 1 Week, 2 Weeks.

Return ONLY valid JSON arrays.

Example:
[
  {{
    "task":"Login Module",
    "priority":"High",
    "description":"Create login page",
    "assigned_user":"{dynamic_team[0] if dynamic_team else 'Sanju'}",
    "time_period":"5 Days"
  }}
]

Requirement Document:
{document_text}
"""
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    print("AI RESPONSE:")
    print(content)

    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    return json.loads(content)
