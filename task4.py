from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from agent.agent import agent
from pathlib import Path
from fastapi import HTTPException
from langchain_community.document_loaders import TextLoader
from rag.rag_pipeline import splitter, vector_db

app = FastAPI()


# Request schema
class ChatRequest(BaseModel):
    message: str
    thread_id: str = "1"


# 1. Chat API
@app.post("/chat")
def chat(request: ChatRequest):

    response = agent.invoke(
        {"messages": [
            {"role": "user", "content": request.message}
        ]},
        config={"configurable": {"thread_id": request.thread_id}}
    )

    return {"response": response["messages"][-1].content}



# 2. Upload doc
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # Accept only text files
    if not file.filename or not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files allowed")

    # Save document in docs folder
    file_path = Path("docs") / Path(file.filename).name

    if file_path.exists():
        raise HTTPException(status_code=409, detail="File already exists")

    content = await file.read()
    file_path.write_bytes(content)

    # Load uploaded document
    loader = TextLoader(str(file_path), encoding="utf-8")
    documents = loader.load()

    # Split document into chunks
    chunks = splitter.split_documents(documents)

    # Store embeddings in ChromaDB
    vector_db.add_documents(chunks)

    return {"message": "Document uploaded successfully"}



    