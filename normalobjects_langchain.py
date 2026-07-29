"""
Evaluate one NormalObjects - Creative Complaint Handler (LangChain) path and prove the answer is 
grounded in inspectable evidence.
Author: Akansha Verma
"""
import time
from dotenv import load_dotenv

import gradio as gr
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from normalobjects_tools import (
    consult_eleven,
    consult_demogorgon,
    check_hawkins_records,
    cast_interdimensional_spell,
    gather_party_wisdom
)

# Load environment variables from .env
load_dotenv()

# 1. Initialize the LLM
setup_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
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
# Gradio UI
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

