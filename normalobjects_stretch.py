from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3) # Lower temp for better guardrail adherence

# ==========================================
# THEMED TOOLS
# ==========================================
@tool
def consult_eleven(question: str) -> str:
    """Consult Eleven regarding psychic disturbances, remote viewing, or emotional states."""
    return f"Eleven (Remote Viewing Output): I feel static and a heavy cold presence near the school."

@tool
def check_hawkins_records(query: str) -> str:
    """Search Hawkins municipal and lab historical records for specific topics."""
    records = {
        "portal": "Record #101: Gate activity spiked near the quarry in 1983.",
        "electricity": "Record #412: Unexplained magnetic and electrical fluctuations reported town-wide."
    }
    for key, record in records.items():
        if key in query.lower():
            return record
    return "Hawkins Records: No matching archive found."

tools = [consult_eleven, check_hawkins_records]

system_prompt = (
    "You are a strict Hawkins incident response agent. "
    "You MUST use at least one tool. You must base your final response strictly "
    "on the evidence returned by the tools. Do not invent outside lore."
)

memory = MemorySaver()
agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt, checkpointer=memory)

# ==========================================
# STRETCH: GUARDRAIL & TRACE VIEW WRAPPER
# ==========================================
def run_with_guardrail_and_trace(query: str):
    config = {"configurable": {"thread_id": "stretch-session"}}
    
    # 1. Execute Agent
    result = agent.invoke({"messages": [HumanMessage(content=query)]}, config)
    
    # 2. Extract Trace and Tool Evidence
    retrieved_evidence = []
    final_output = ""
    
    print("\n" + "="*40)
    print("🔍 INSPECTABLE TRACE VIEW")
    print("="*40)
    
    for msg in result["messages"]:
        if msg.type == "human":
            print(f"[User Query]: {msg.content}")
        elif isinstance(msg, AIMessage) and msg.tool_calls:
            print(f"[Tool Call]: {msg.tool_calls[0]['name']} (Args: {msg.tool_calls[0]['args']})")
        elif msg.type == "tool":
            print(f"[Tool Evidence Retrieved]: {msg.content}")
            retrieved_evidence.append(msg.content)
        elif msg.type == "ai" and not msg.tool_calls:
            final_output = msg.content
            print(f"\n[Raw AI Output]:\n{final_output}")
            
    print("="*40)

    # 3. Guardrail Check (Post-Generation Verification)
    print("🛡️ [Guardrail Validation Status]:")
    if not retrieved_evidence:
        print("-> WARNING: Zero tools invoked! Guardrail triggered: Response unverified.")
    else:
        evidence_text = " ".join(retrieved_evidence).lower()
        key_terms = [word for word in ["record", "eleven", "gate", "quarry", "magnetic", "electrical"] if word in evidence_text]
        
        grounded = any(term in final_output.lower() for term in key_terms)
        if grounded:
            print("-> PASSED: Final answer is structurally grounded in tool evidence.")
        else:
            print("-> FAILED: Guardrail detected potential hallucination from unsupported text.")
    print("="*40 + "\n")

if __name__ == "__main__":
    print("Running Stretch Test with Guardrail & Trace Inspection...")
    run_with_guardrail_and_trace("The power grid is failing and my compass is broken near the school!")