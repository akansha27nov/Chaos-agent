import os
import random
from dotenv import load_dotenv
from typing import List, Dict

from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Load environment variables from .env
load_dotenv()

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

# ==========================================
# TOOL VALIDATION
# ==========================================
if __name__ == "__main__":
    print("--- Validating Tool Signatures & Output Types ---")
    print("1. Demogorgon Tool:", consult_demogorgon.invoke({"complaint": "The lights are flickering"}))
    print("2. Hawkins Records Tool:", check_hawkins_records.invoke({"query": "Check portal records"}))
    print("3. Spell Casting Tool:\n", cast_interdimensional_spell.invoke({"problem": "Broken elevator", "creativity_level": "high"}))
    print("4. Party Wisdom Tool:", gather_party_wisdom.invoke({"question": "Are there monsters outside?"}))
    print("--- All Chunk 1 Tools Validated Successfully ---")

