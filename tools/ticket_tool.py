import json
from pathlib import Path
from pydantic import BaseModel, Field
from langchain.tools import tool

# Path to tickets.json
TICKET_FILE = Path(__file__).resolve().parent.parent / "data" / "tickets.json"


# 1. Pydantic schema
class Ticket(BaseModel):
    ticket_id: str
    issue: str = Field(min_length=1)


# 2. Create Support Ticket Tool
@tool
def create_ticket(issue: str) -> str:
    """Create a support ticket for a customer complaint."""

    # Read existing tickets from JSON
    with open(TICKET_FILE, "r", encoding="utf-8") as file:
        tickets = json.load(file)

    # Create ticket with ID and validate using Pydantic
    ticket = Ticket(
        ticket_id=f"T{len(tickets) + 1:03d}",
        issue=issue.strip()
    )

    # Add new ticket to Python list
    tickets.append(ticket.model_dump())

    # Save updated list back to JSON
    with open(TICKET_FILE, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)  # Python object to JSON file.

    return "Support ticket created successfully"


# 3. Test
if __name__ == "__main__":
    print(create_ticket.invoke({"issue": "My package is delayed"}))