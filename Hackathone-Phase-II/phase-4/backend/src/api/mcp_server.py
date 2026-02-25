"""
MCP (Model Context Protocol) Server Implementation for the Todo Backend API.

Implements the MCP server with 5 task management tools using the Official MCP SDK.
"""
from mcp.server import Server
from mcp.types import CallToolResult, Tool
from typing import Dict, Any, List
import json
from sqlmodel import create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager

from ..models.user import UserRead
from ..services.task_service import TaskService
from ..services.ai_service import ai_service


# Create the MCP server instance
server = Server("todo-mcp-server")



@server.list_tools()
async def list_tools() -> List[Tool]:
    """List all available tools in the MCP server."""
    return [
        Tool(
            name="add_task",
            description="Create a new task",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User identifier"},
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description (optional)"}
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="Retrieve tasks from the list",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User identifier"},
                    "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter by status"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as complete",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User identifier"},
                    "task_id": {"type": "integer", "description": "Task ID to complete"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Remove a task from the list",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User identifier"},
                    "task_id": {"type": "integer", "description": "Task ID to delete"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Modify task title or description",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User identifier"},
                    "task_id": {"type": "integer", "description": "Task ID to update"},
                    "title": {"type": "string", "description": "New title (optional)"},
                    "description": {"type": "string", "description": "New description (optional)"}
                },
                "required": ["user_id", "task_id"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """
    Handle tool calls from the MCP server.

    Args:
        name: Name of the tool to call
        arguments: Arguments to pass to the tool

    Returns:
        Result of the tool call
    """
    try:
        # Extract user_id from arguments
        user_id = int(arguments.get("user_id"))

        # Create a mock user object for compatibility with existing services
        # In a real implementation, you would fetch the user from the database
        current_user = UserRead(
            id=user_id,
            email=f"user_{user_id}@example.com"  # Placeholder email
        )

        # Get the database session - in a real implementation, you would get this properly
        # For now, we'll use the AI service which handles the database operations
        if name == "add_task":
            title = arguments.get("title")
            description = arguments.get("description")

            # Using the AI service's method for consistency
            result = await ai_service.add_task_tool(
                title=title,
                description=description,
                user=current_user,
                session=None  # Will be handled internally
            )

            return CallToolResult(content=json.dumps(result))

        elif name == "list_tasks":
            status = arguments.get("status", "all")

            # Using the AI service's method for consistency
            result = await ai_service.list_tasks_tool(
                user=current_user,
                session=None  # Will be handled internally
            )

            # Filter results based on status if needed
            if status != "all" and "tasks" in result:
                if status == "pending":
                    result["tasks"] = [task for task in result["tasks"] if not task.get("completed")]
                elif status == "completed":
                    result["tasks"] = [task for task in result["tasks"] if task.get("completed")]

            return CallToolResult(content=json.dumps(result))

        elif name == "complete_task":
            task_id = arguments.get("task_id")

            # Using the AI service's method for consistency
            result = await ai_service.complete_task_tool(
                task_id=task_id,
                user=current_user,
                session=None  # Will be handled internally
            )

            return CallToolResult(content=json.dumps(result))

        elif name == "delete_task":
            task_id = arguments.get("task_id")

            # Using the AI service's method for consistency
            result = await ai_service.delete_task_tool(
                task_id=task_id,
                user=current_user,
                session=None  # Will be handled internally
            )

            return CallToolResult(content=json.dumps(result))

        elif name == "update_task":
            task_id = arguments.get("task_id")
            title = arguments.get("title")
            description = arguments.get("description")

            # Using the AI service's method for consistency
            result = await ai_service.update_task_tool(
                task_id=task_id,
                title=title,
                description=description,
                user=current_user,
                session=None  # Will be handled internally
            )

            return CallToolResult(content=json.dumps(result))

        else:
            return CallToolResult(
                content=json.dumps({
                    "success": False,
                    "error": f"Unknown tool: {name}",
                    "message": f"Tool '{name}' not found"
                })
            )

    except Exception as e:
        return CallToolResult(
            content=json.dumps({
                "success": False,
                "error": str(e),
                "message": f"Error executing tool {name}: {str(e)}"
            })
        )


# For standalone execution
if __name__ == "__main__":
    import asyncio
    import argparse

    parser = argparse.ArgumentParser(description="Run the Todo MCP Server")
    parser.add_argument("--port", type=int, default=3000, help="Port to run the server on")
    args = parser.parse_args()

    async def main():
        # Start the server
        await server.run(port=args.port)

    asyncio.run(main())