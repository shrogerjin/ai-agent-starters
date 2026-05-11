"""AI Agent Core - Autonomous agent with tool use and memory."""
import asyncio
import logging
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """A message in the conversation."""
    role: str  # "user", "assistant", "system", "tool"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    tool_calls: Optional[List[Dict]] = None


@dataclass
class Tool:
    """A tool available to the agent."""
    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any]


class Agent:
    """Autonomous agent with tool use capabilities."""

    def __init__(self, name: str = "Assistant", model: str = "gpt-4"):
        self.name = name
        self.model = model
        self.messages: List[Message] = []
        self.tools: Dict[str, Tool] = {}
        self.memory: List[Dict] = []
        self.max_memory = 100

    def tool(self, name: str = None, description: str = "", parameters: Dict = None):
        """Decorator to register a tool."""
        def decorator(func: Callable):
            tool_name = name or func.__name__
            self.tools[tool_name] = Tool(
                name=tool_name,
                description=description or func.__doc__ or "",
                function=func,
                parameters=parameters or {}
            )
            logger.info(f"Registered tool: {tool_name}")
            return func
        return decorator

    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        msg = Message(role=role, content=content)
        self.messages.append(msg)
        
        # Manage memory
        if len(self.messages) > self.max_memory:
            self.messages = self.messages[-self.max_memory:]
        
        return msg

    async def think(self, prompt: str) -> str:
        """Make a reasoning step - in production, call LLM API."""
        self.add_message("user", prompt)
        
        # Simulate reasoning - in production, call actual LLM
        response = f"Agent thinking about: {prompt[:50]}..."
        self.add_message("assistant", response)
        
        return response

    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool by name."""
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found"
        
        tool = self.tools[tool_name]
        try:
            result = await tool.function(**kwargs) if asyncio.iscoroutinefunction(tool.function) \
                else tool.function(**kwargs)
            return result
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return f"Error executing {tool_name}: {str(e)}"

    async def run(self, task: str, max_iterations: int = 5) -> str:
        """Run the agent on a task autonomously."""
        self.add_message("system", f"You are {self.name}, an autonomous agent.")
        
        for i in range(max_iterations):
            logger.info(f"Iteration {i+1}/{max_iterations}: {task}")
            
            thought = await self.think(task)
            logger.info(f"Thought: {thought}")
            
            # Check if task is complete
            if any(word in thought.lower() for word in ["done", "complete", "finished", "resolved"]):
                return thought
            
            # Try to use a tool if mentioned
            for tool_name in self.tools:
                if tool_name in thought.lower():
                    result = await self.execute_tool(tool_name)
                    self.add_message("tool", f"{tool_name}: {result}")
        
        return "Max iterations reached"

    def get_conversation_history(self) -> List[Dict]:
        """Get formatted conversation history."""
        return [
            {"role": m.role, "content": m.content, "timestamp": m.timestamp.isoformat()}
            for m in self.messages
        ]
