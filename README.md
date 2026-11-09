# AI Customer Support Assistant

An AI-powered customer support backend built using **FastAPI, LangChain, LangGraph, Groq, and ChromaDB**.

The application combines **Retrieval-Augmented Generation (RAG)** with AI agents to answer customer queries, retrieve company policies, track orders, and create support tickets.

## Features

- **RAG-based Question Answering:** Retrieves relevant information from FAQs, shipping details, and return policies.
- **AI Agent with Tool Calling:** Automatically selects the appropriate tool based on the customer's request.
- **Order Tracking:** Retrieves order information using an order ID.
- **Support Ticket Creation:** Creates and stores customer support tickets.
- **Conversation Memory:** Maintains conversation context using LangGraph's in-memory checkpointer.
- **Document Upload:** Supports uploading `.txt` documents and adding their embeddings to ChromaDB.
- **REST APIs:** Provides chat and document upload endpoints through FastAPI.

## Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend | FastAPI, Pydantic |
| AI Frameworks | LangChain, LangGraph |
| LLM | Groq (GPT-OSS-20B) |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Vector Database | ChromaDB |
| Data Storage | JSON files |
| API Testing | Swagger UI |

## Project Structure

```text
AI-Customer-Support-Assistant/
├── agent/
│   └── agent.py
├── rag/
│   └── rag_pipeline.py
├── tools/
│   ├── order_tool.py
│   └── ticket_tool.py
├── data/
│   ├── orders.json
│   └── tickets.json
├── docs/
│   ├── faq.txt
│   ├── return_policy.txt
│   └── shipping_info.txt
├── task4.py
├── requirements.txt
├── .env.example
└── README.md
```

## How It Works

1. A customer sends a message through the FastAPI `/chat` endpoint.
2. The LangChain agent analyzes the request and selects the appropriate tool.
3. For policy questions, the RAG pipeline retrieves relevant document chunks from ChromaDB.
4. For order tracking or support tickets, the agent accesses the corresponding JSON-based tools.
5. The LLM generates a response using the available information.
6. LangGraph maintains conversation context using a thread ID during the running application session.

## Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/Yash-Kumar-githb/AI-Customer-Support-Assistant.git
cd AI-Customer-Support-Assistant
```

**2. Create and activate a virtual environment**

Python 3.12 is recommended for the current pinned dependencies.

Windows PowerShell:

```powershell
py -3.12 -m venv AI-Cutomer-Env
.\AI-Cutomer-Env\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root using `.env.example` as a reference.

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit your `.env` file or API keys to GitHub.

**5. Start the FastAPI server**

```bash
fastapi dev task4.py
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

### POST /chat

Sends a customer message to the AI agent.

Example request:

```json
{
  "message": "What is the return policy?",
  "thread_id": "user-1"
}
```

The API returns an AI-generated response in the `response` field.

Use the same `thread_id` for follow-up messages in a conversation.

### POST /upload

Uploads a new `.txt` document into the knowledge base.

- Accepts a file using `multipart/form-data`.
- Saves the file in the `docs/` directory.
- Splits the document into chunks.
- Generates embeddings and adds them to ChromaDB.
- Rejects unsupported file extensions and duplicate filenames.

## Current Limitations

- Only `.txt` document uploads are supported.
- Orders and support tickets use local JSON files.
- Conversation memory is stored in RAM and resets when the server restarts.
- Uploaded documents require additional handling for updating or deleting existing embeddings.
- The application is a development/demo project and is not production-ready.

## Future Improvements

- Support PDF and DOCX documents.
- Use PostgreSQL and SQLAlchemy for orders and tickets.
- Implement persistent conversation memory.
- Improve document update and deletion handling.
- Add authentication, validation, and automated tests.

## Author

Developed by [Yash Kumar](https://github.com/Yash-Kumar-githb).
