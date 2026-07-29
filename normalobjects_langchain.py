import os
import random
from dotenv import load_dotenv
from typing import List, Dict

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables from .env
load_dotenv()

# 1. Initialize the LLM
setup_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# ==========================================
# Step 2: Create Creative Tools
# ==========================================

@tool
def consult_demogorgon(complaint: str) -> str:
    """Consult the Demogorgon about a complaint regarding the Upside Down."""
    responses: List[str] = [
        f"Gurgle... *screech*! Translation: The Demogorgon finds '{complaint}' hilarious and wants to turn it into slime.",
        f"*Low growl*... The Demogorgon demands more waffle sacrifices before addressing '{complaint}'.",
        f"RAAAGH! The Demogorgon drags your complaint '{complaint}' straight into the Upside Down!"
    ]
    return random.choice(responses)

@tool
def check_hawkins_records(query: str) -> str:
    """Search Hawkins municipal and lab historical records for specific topics."""
    records: Dict[str, str] = {
        "portal": "Record #101: Gate activity spiked near the quarry in 1983. Energy levels off the charts.",
        "monsters": "Record #204: Multiple sightings of bipedal floral-headed entities near Mirkwood.",
        "psychics": "Record #309: Hawkins National Lab Subject 011 demonstrated telekinetic capabilities.",
        "electricity": "Record #412: Unexplained magnetic and electrical fluctuations reported town-wide."
    }
    query_lower = query.lower()
    for key, record in records.items():
        if key in query_lower:
            return record
    return "Hawkins Records: No matching archive found for your query."

@tool
def cast_interdimensional_spell(problem: str, creativity_level: str = "medium") -> str:
    """Cast an interdimensional spell to solve a problem with low, medium, or high creativity."""
    multipliers: Dict[str, int] = {"low": 1, "medium": 2, "high": 3}
    count = multipliers.get(creativity_level.lower(), 2)
    
    spells: List[str] = [
        f"Banishment Beam: Channeling energy to erase '{problem}' from this dimension.",
        f"Temporal Loophole: Rewinding time 5 minutes to prevent '{problem}' from happening.",
        f"Ego Transmutation: Turning '{problem}' into a harmless pile of damp autumn leaves.",
        f"Shadow Shield: Enclosing '{problem}' in a void barrier until next Tuesday."
    ]
    selected = random.sample(spells, min(count, len(spells)))
    return "\n".join(selected)

@tool
def gather_party_wisdom(question: str) -> str:
    """Gather advice and insights from the Hawkins party members (Mike, Dustin, Lucas, Will)."""
    party_responses: Dict[str, str] = {
        "portal": "Mike: 'We need to keep Eleven away from the gate unless it's an emergency!'",
        "monsters": "Dustin: 'I've checked the D&D Monster Manual—this matches a Thessalhydra behavior pattern!'",
        "psychics": "Will: 'I can feel it in the back of my neck... it's close.'",
        "electricity": "Lucas: 'Get your wrist-rockets ready! If the lights flicker, we move!'"
    }
    question_lower = question.lower()
    for key, response in party_responses.items():
        if key in question_lower: 
            return response
    return "Party Huddle: The gang gathers around the walkie-talkies to brainstorm a workaround."

@tool
def consult_eleven(question:str) -> str:
    """Consult Eleven regarding psychic disturbances, remote viewing, or emotional states."""
    # Extension Feature: Uses an internal LLM call for a dynamic, context-aware response
    dynamic_prompt = f"You are Eleven from Stranger Things. Answer this question/complaint psychically and briefly: '{question}'"
    response = setup_model.invoke(dynamic_prompt)
    return f"Eleven (Remote Viewing Output): {response.content}"
    
# ==========================================
# Step 3: Create Agent with Tools
# ==========================================

# 2. Package Tools
tools = [
    consult_eleven,
    consult_demogorgon,
    check_hawkins_records,
    cast_interdimensional_spell,
    gather_party_wisdom
]

# 3. Create System Prompt 
system_prompt = (
    "You are a chaotic but helpful incident response agent in the town of Hawkins. "
    "When handling a complaint, you must use at least one tool to investigate the issue or find a solution. "
    "Synthesize the tool's output into a highly creative, slightly unhinged final response."
)

system_prompt_1 = (
    "You are a chaotic but helpful incident response agent in the town of Hawkins. "
    "Use tools when investigating issues, and maintain continuity using conversation memory."
)

# Initialize short-term memory checkpointer for multi-turn threads
memory = MemorySaver()

# 4. create agent
agent = create_agent(
    model=setup_model, 
    tools=tools, 
    system_prompt=system_prompt_1,
    checkpointer=memory
)

# ==========================================
# Agent Validation
# ==========================================
if __name__ == "__main__":
    print("\n--- Testing Agent Execution ---")
    test_complaint = "The electricity in my house is flickering and my compass is pointing the wrong way!"
    print(f"INPUT: {test_complaint}\n")
    # Add config
    config = {"configurable": {"thread_id": "lab-proof-session"}}
    result = agent.invoke({"messages": [{"role": "user", "content": test_complaint}]}, config)
    
    print("==========================================")
    
    for msg in result["messages"]:
        if msg.type == "human":
            print(f"INPUT (Query): {msg.content}")
        elif msg.type == "ai" and msg.tool_calls:
            print(f"DECIDE (Tool Call): {msg.tool_calls[0]['name']} | Args: {msg.tool_calls[0]['args']}")
        elif msg.type == "tool":
            print(f"VERIFY (Tool Evidence): {msg.content}")
        elif msg.type == "ai" and not msg.tool_calls:
            print(f"\nBUILD (Final Output):\n{msg.content}")
    print("==========================================\n")
    
    print("\n--- Extension Turn 1: Initial Complaint ---")
    q1 = "My house lights are flickering constantly!"
    print(f"User: {q1}")
    res1 = agent.invoke(
        {"messages": [{"role": "user", "content": q1}]}, 
        config
    )
    print(f"Agent:\n{res1['messages'][-1].content}\n")
    
    print("--- Extension Turn 2: Follow-up using Memory & New Dynamic Tool ---")
    q2 = "Can you ask Eleven what she senses about that issue?"
    print(f"User: {q2}")
    res2 = agent.invoke(
            {"messages": [{"role": "user", "content": q2}]}, 
            config
        )
    print(f"Agent:\n{res2['messages'][-1].content}\n")
    

