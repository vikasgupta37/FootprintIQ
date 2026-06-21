"""
AI Tool Registry.
Registers tools with their schemas and execution handlers.
"""

from typing import Any, Callable, Coroutine, Dict, List, Tuple
from app.core.logging import logger

# Tool Handler Type: async function that takes (db_session, user, tool_arguments) and returns a dict
ToolHandler = Callable[..., Coroutine[Any, Any, Dict[str, Any]]]

class ToolRegistry:
    """Registry for AI Agent tools to enforce Open/Closed Principle."""
    
    _tools: Dict[str, Tuple[Dict[str, Any], ToolHandler]] = {}

    @classmethod
    def register(cls, name: str, schema: Dict[str, Any], handler: ToolHandler):
        """Register a tool schema and its execution handler."""
        cls._tools[name] = (schema, handler)
        logger.info(f"Registered AI tool: {name}")

    @classmethod
    def get_all_schemas(cls) -> List[Dict[str, Any]]:
        """Return all registered tool schemas in Anthropic format."""
        schemas = []
        for name, (schema, _) in cls._tools.items():
            # Wrap the schema in the format Anthropic expects
            schemas.append({
                "name": name,
                "description": schema.get("description", ""),
                "input_schema": schema.get("input_schema", {})
            })
        return schemas

    @classmethod
    async def execute(cls, name: str, db: Any, user: Any, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool by name."""
        if name not in cls._tools:
            error_msg = f"Tool {name} not found in registry"
            logger.error(error_msg)
            return {"error": error_msg}

        _, handler = cls._tools[name]
        try:
            logger.info(f"Executing tool: {name} with args: {arguments}")
            return await handler(db, user, arguments)
        except Exception as e:
            logger.error(f"Error executing tool {name}: {e}")
            return {"error": str(e)}

registry = ToolRegistry()
