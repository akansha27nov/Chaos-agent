import os
import random
import time
from dotenv import load_dotenv
from typing import List, Dict

import gradio as gr
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
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
# PERFORMANCE METRICS WRAPPER & CHAT HANDLER
# ==========================================
def run_agent_with_metrics(user_message, history):
    config = {"configurable": {"thread_id": "gradio-ui-session"}}
    
    # Start performance timer
    start_time = time.time()
    
    # Invoke agent graph
    result = agent.invoke({"messages": [HumanMessage(content=user_message)]}, config)
    
    # End performance timer
    duration = time.time() - start_time
    
    # Analyze tool usage efficiency from message history
    tools_called = []
    for msg in result["messages"]:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for tc in msg.tool_calls:
                tools_called.append(tc['name'])
                
    ai_response = result["messages"][-1].content
    
    # Format a performance metrics badge to append or log
    metrics_info = f"\n\n*(Performance: {duration:.2f}s | Tools Used: {tools_called if tools_called else 'None'})*"
    
    return ai_response + metrics_info

# ==========================================
# GRADIO WEB INTERFACE
# ==========================================
demo = gr.ChatInterface(
    fn=run_agent_with_metrics,
    title="🚨 Hawkins Incident Response & Chaos Agent",
    description="Ask complaints about Hawkins, consult Eleven or the Demogorgon, and test memory persistence across turns. Performance metrics are logged per message.",
    textbox=gr.Textbox(placeholder="E.g., My house lights are flickering! What should I do?", container=False, scale=7),
    theme="soft",
)

if __name__ == "__main__":
    print("Launching Gradio interface locally...")
    demo.launch()

