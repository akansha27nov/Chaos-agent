import os
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

