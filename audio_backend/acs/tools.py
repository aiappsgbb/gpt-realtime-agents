import sys
from pathlib import Path
print(f"Sys importing {str(Path(__file__).parent )}")
sys.path.insert(0, str(Path(__file__).parent ))

import json
from typing import Any
from enum import Enum
from typing import Any, Callable

class ToolResultDirection(Enum):
    TO_SERVER = 1
    TO_CLIENT = 2

class ToolResult:
    text: str
    destination: ToolResultDirection

    def __init__(self, text: str, destination: ToolResultDirection):
        self.text = text
        self.destination = destination

    def to_text(self) -> str:
        if self.text is None:
            return ""
        return self.text if type(self.text) == str else json.dumps(self.text)

class Tool:
    target: Callable[..., ToolResult]
    schema: Any

    def __init__(self, target: Any, schema: Any):
        self.target = target
        self.schema = schema

class RTToolCall:
    tool_call_id: str
    previous_id: str

    def __init__(self, tool_call_id: str, previous_id: str):
        self.tool_call_id = tool_call_id
        self.previous_id = previous_id


def register_tools_from_registry(rtmt: Any, tools_registry: dict) -> None:
    """
    Convert TOOLS_REGISTRY format to Tool instances and register them with rtmt.
    
    Args:
        rtmt: The RTMiddleTier instance to register tools with
        tools_registry: Dictionary mapping tool names to their definitions and executors
        
    Example:
        TOOLS_REGISTRY = {
            "tool_name": {
                "definition": {...},  # OpenAI function definition
                "executor": function_reference
            }
        }
    """
    for tool_name, tool_config in tools_registry.items():
        rtmt.tools[tool_name] = Tool(
            target=tool_config["executor"],
            schema=tool_config["definition"]
        )
