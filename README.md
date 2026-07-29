# Hawkins Incident Response & Chaos Agent

A modular LangChain and LangGraph agent that processes chaotic appliance complaints through a Stranger Things theme, featuring shared tool management, conversation memory, a Gradio chat interface, and a dedicated guardrail trace validation workflow.

## Project Structure
```
Chaos-agent/
├── normalobjects_tools.py        # Shared tool registry (consult_eleven, demogorgon, records, spells, party wisdom)
├── normalobjects_langchain.py    # Gradio chat UI wrapper with memory (MemorySaver) and performance metrics
├── normalobjects_stretch.py      # Stretch CLI script for inspectable traces and guardrail validation
├── screenshots/                  # Screenshots of various outputs (from terminal and UI)
├── lab_proof.md                  # Proof of learning
├── .env                          # OPENAI_API_KEY (not committed)
└── .gitignore
```

## Setup
1. Activate your Python environment (e.g., conda):
```bash
conda activate bootcamp-env
```
2. Install dependencies:
```bash
pip install langchain langchain-openai langchain-core langgraph gradio python-dotenv
```
3. Make sure your `.env` file contains your OpenAI API key:
```bash
OPENAI_API_KEY=your-key-here
```

## Running the Web Interface
```bash
conda activate bootcamp-env
python normalobjects_langchain.py
```

Launches a localized Gradio chat interface. Conversation history and state persist across turns using LangGraph's MemorySaver checkpointer, while response times and tool usage efficiency metrics are calculated per message.

## Running the Guardrail & Trace Test
```bash
conda activate bootcamp-env
python normalobjects_stretch.py
```
Executes the strict stretch workflow. This runs a sample complaint through an isolated agent and outputs an inspectable trace view (`[User Query]`, `[Tool Call]`, `[Tool Evidence Retrieved]`, `[Raw AI Output]`) alongside post-generation guardrail validation checks.

## Tools
| Tool | What it does |
|---|---|
| `consult_eleven` | Consults Eleven regarding psychic disturbances, leveraging an internal LLM call for dynamic context |
| `consult_demogorgon` | Returns randomized chaotic responses or slime/waffle demands regarding the Upside Down |
| `check_hawkins_records` | Keyword-matched lookup across municipal and lab historical records (portal, monsters, psychics, electricity) |
| `cast_interdimensional_spell` | Selects N random spell effects based on a chosen creativity level (low, medium, high) |
| `gather_party_wisdom` | Pulls character-voiced advice and insights from Hawkins party members (Mike, Dustin, Lucas, Will) |

