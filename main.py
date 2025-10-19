from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("AIPIPE_TOKEN"),
    base_url="https://aipipe.org/openrouter/v1"
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_ticket_status",
            "description": "Retrieves the status of an IT support ticket",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "integer",
                        "description": "The unique ticket identifier"
                    }
                },
                "required": ["ticket_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_meeting",
            "description": "Schedules a meeting for a specific date, time, and room",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Meeting date in YYYY-MM-DD format"
                    },
                    "time": {
                        "type": "string",
                        "description": "Meeting time in HH:MM format"
                    },
                    "meeting_room": {
                        "type": "string",
                        "description": "Name or identifier of the meeting room"
                    }
                },
                "required": ["date", "time", "meeting_room"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_expense_balance",
            "description": "Retrieves the current expense reimbursement balance for an employee",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "integer",
                        "description": "The unique employee identifier"
                    }
                },
                "required": ["employee_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_performance_bonus",
            "description": "Calculates the performance bonus for an employee for a specific year",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "integer",
                        "description": "The unique employee identifier"
                    },
                    "current_year": {
                        "type": "integer",
                        "description": "The year for which to calculate the bonus"
                    }
                },
                "required": ["employee_id", "current_year"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "report_office_issue",
            "description": "Reports an office issue with a specific issue code and department",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue_code": {
                        "type": "integer",
                        "description": "The unique issue identifier code"
                    },
                    "department": {
                        "type": "string",
                        "description": "The department responsible for handling the issue"
                    }
                },
                "required": ["issue_code", "department"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

@app.get("/execute")
async def execute(q: str):
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": q}],
        tools=tools,
        tool_choice="required"
    )
    
    tool_call = response.choices[0].message.tool_calls[0]
    
    return {
        "name": tool_call.function.name,
        "arguments": tool_call.function.arguments
    }

@app.get("/")
async def root():
    return {"status": "running"}
