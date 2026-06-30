import os
import json
from openai import OpenAI

# Initialize the secure production-ready gateway pipeline client wrapper
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")  # Dynamically loaded via Cloud Environment configurations
)

def generate_tasks(document_text):

    prompt = f"""
You are acting as a Software Project Manager.

Distribute tasks fairly across the following six team members.

Rules:

1. Every task must be assigned.
2. Balance the workload.
3. Do not assign more than two consecutive tasks to the same member.
4. Use expertise first.
5. If multiple people are suitable, choose the person with the fewest assigned tasks.
6. At the end, every member should have a similar number of tasks whenever possible.
Team Members:

Sanju
- Python
- Backend
- AI

Joanna
- React
- Frontend
- UI
- UX

Sahana
- QA
- Testing
- Documentation

Pradeep
- MongoDB
- Database
- APIs
- Backend

Rakshanaa
- Analytics
- Reports
- Dashboard

Parkavi
- Deployment
- DevOps
- Bug Fixing

IMPORTANT RULES

Every task MUST contain ALL FIVE fields.

task

priority

description

assigned_user

time_period

Never omit any field.

Never leave any field blank.

time_period must be one of:

1 Day
2 Days
3 Days
5 Days
1 Week
2 Weeks

Return ONLY valid JSON.

Example:

[
{{
"task":"Login Module",
"priority":"High",
"description":"Create login page",
"assigned_user":"Pradeep",
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
