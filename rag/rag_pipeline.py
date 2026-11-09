
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pathlib import Path

load_dotenv()


# 1. Load documents
files = list(Path("docs").glob("*.txt"))



documents = []

for file in files:
    loader = TextLoader(file, encoding="utf-8")
    documents.extend(loader.load())

# print("Total documents:", len(documents))


# 2. Split documents into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)


# print("Total chunks:", len(chunks))

# for chunk in chunks:
#     print(chunk.page_content)



# 3. Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Store chunks in ChromaDB

vector_db = Chroma(
    collection_name="support_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

if not vector_db.get(limit=1)["ids"]:
    vector_db.add_documents(chunks)
    print("Chunks stored successfully")





llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)



def ask_rag(question: str):
    docs = vector_db.similarity_search(question, k=2)

    context = "\n".join(doc.page_content for doc in docs)

    response = llm.invoke(
        f"""Answer the question using only the context below.
        If the answer is not present, say you don't know.

        Context:
        {context}

        Question:
        {question}"""
    )

    return response.content


# Test
if __name__ == "__main__":
    print(ask_rag("What is the return policy?"))