"""Configuration for AI agent."""
import os

# LLM Settings
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai, anthropic, local
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
LLM_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "")

# Agent Settings
AGENT_NAME = "Assistant"
AGENT_MAX_ITERATIONS = 10
AGENT_TIMEOUT = 300

# Memory Settings
MEMORY_MAX_ITEMS = 1000
MEMORY_ENABLED = True

# Tool Settings
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "")
