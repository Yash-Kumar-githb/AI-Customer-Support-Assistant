
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

from rag.rag_pipeline import ask_rag
from tools.order_tool import check_order_status
from tools.ticket_tool import create_ticket

load_dotenv()


# 1. Initialize LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# 2. Convert RAG function into a tool
@tool
def search_knowledge_base(question: str) -> str:
    """Search company documents for FAQs, returns, refunds and shipping policies."""
    return ask_rag(question)


# 3. Create conversation memory
memory = InMemorySaver()


# 4. Create agent with all 3 tools
agent = create_agent(
    model=llm,
    tools=[
        search_knowledge_base,
        check_order_status,
        create_ticket
    ],
    checkpointer=memory,
    system_prompt=(
        "You are an e-commerce customer support assistant. "
        "Always use the knowledge base tool for company policy questions. "
        "Use check_order_status for order tracking. "
        "Use create_ticket when the user requests a support ticket. "
        "For mixed questions, use all relevant tools. "
        "Never invent company policies or order details."
    )
)


# 5. Test agent
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "1"}}

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        response = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config
        )

        print("Agent:", response["messages"][-1].content)
