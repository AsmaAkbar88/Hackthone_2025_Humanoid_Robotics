"""
Chat API routes for the Todo Backend API.

Implements the chat endpoint using FastAPI.
"""
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel

from ...models.user import UserRead
from ...models.conversation import Conversation, ConversationCreate
from ...models.message import Message, MessageCreate, MessageRole
from ...services.conversation_service import ConversationService
from ...services.ai_service import ai_service
from ...database.database import get_async_session
from ...middleware.chat_auth import chat_auth


router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    success: bool
    data: Dict[str, Any]


@router.post("/{user_id}", response_model=ChatResponse)
async def chat_with_ai(
    user_id: int,
    chat_request: ChatRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Process natural language input from user and return AI-generated response with appropriate task operations.
    
    Args:
        user_id: ID of the authenticated user
        chat_request: Chat request containing message and optional conversation_id
        session: Async database session
        
    Returns:
        Dictionary containing AI response and any actions taken
    """
    try:
        # Verify user authentication and authorization
        # In a real implementation, we would get the token from the request headers
        # For now, we'll retrieve the user from the database
        from sqlmodel import select
        from ...models.user import User
        user_statement = select(User).where(User.id == user_id)
        user_result = await session.execute(user_statement)
        db_user = user_result.scalar_one_or_none()
        
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        current_user = UserRead.model_validate(db_user)
        
        # Get or create conversation
        if chat_request.conversation_id:
            # Load existing conversation
            conversation = await ConversationService.get_conversation_by_id(
                session, chat_request.conversation_id, user_id
            )
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )
        else:
            # Create new conversation
            conversation_data = ConversationCreate(title=chat_request.message[:50] + "..." if len(chat_request.message) > 50 else chat_request.message, user_id=user_id)
            conversation = await ConversationService.create_conversation(session, conversation_data)
        
        # Save user message to conversation
        user_message = MessageCreate(
            role=MessageRole.USER,
            content=chat_request.message,
            conversation_id=conversation.id
        )
        await ConversationService.add_message_to_conversation(session, user_message)
        
        # Process the message with AI service
        # In a real implementation, we would use the OpenAI Agent to determine
        # which MCP tools to call based on the user's natural language
        # For this implementation, we'll simulate natural language processing
        
        # Get the previous messages to understand the context
        # At this point, the current user message has already been added to the conversation
        # So we need to get all messages and exclude the current one
        all_messages = await ConversationService.get_messages_by_conversation_id(session, conversation.id)
        
        # Filter out the current user message that was just added
        # We identify it by matching both content and role
        previous_messages = [
            msg for msg in all_messages 
            if not (msg.content == chat_request.message and msg.role == MessageRole.USER)
        ]
        
        # Check if the user is replying to a specific prompt (like after choosing option 1 to add a task)
        if previous_messages:
            last_assistant_msg = None
            # Find the last assistant message before the current user message
            for msg in reversed(previous_messages):
                if msg.role == MessageRole.ASSISTANT:
                    last_assistant_msg = msg
                    break
            
            # If the last assistant message was asking for a task title (after option 1)
            if last_assistant_msg and ("provide the task title" in last_assistant_msg.content.lower() or 
                                       "add your task now" in last_assistant_msg.content.lower()):
                # This means the user is now providing the task title
                task_title = chat_request.message.strip()
                
                # Call the add_task_tool
                result = await ai_service.add_task_tool(task_title, current_user, session, None)
                if result["success"]:
                    ai_response = f"Task added: {result['message']}"
                    actions_taken = [{
                        "action": "task_created",
                        "task_id": result["task_id"],
                        "details": result["message"]
                    }]
                else:
                    ai_response = f"Failed to add task: {result['message']}"
            
            # If the last assistant message was asking to select a task to complete
            elif last_assistant_msg and "mark as complete" in last_assistant_msg.content.lower():
                # Extract task ID from user's response
                import re
                task_id_match = re.search(r'\b(\d+)\b', chat_request.message)
                if task_id_match:
                    task_id = int(task_id_match.group(1))
                    # Call the complete_task_tool
                    result = await ai_service.complete_task_tool(task_id, current_user, session)
                    if result["success"]:
                        status_text = "completed" if result["completed"] else "marked as incomplete"
                        ai_response = result["message"]
                        actions_taken = [{
                            "action": "task_completed",
                            "task_id": task_id,
                            "details": f"Task {status_text}"
                        }]
                    else:
                        ai_response = f"Failed to complete task: {result['message']}"
                else:
                    ai_response = "Invalid task number. Please select a valid task number from the list."
            
            
            # If the last assistant message was asking to select a task to delete
            elif last_assistant_msg and "delete" in last_assistant_msg.content.lower():
                # Extract task ID from user's response
                import re
                task_id_match = re.search(r'\b(\d+)\b', chat_request.message)
                if task_id_match:
                    task_id = int(task_id_match.group(1))
                    # Call the delete_task_tool
                    result = await ai_service.delete_task_tool(task_id, current_user, session)
                    if result["success"]:
                        ai_response = result["message"]
                        actions_taken = [{
                            "action": "task_deleted",
                            "task_id": task_id,
                            "details": result["message"]
                        }]
                    else:
                        ai_response = f"Failed to delete task: {result['message']}"
                else:
                    ai_response = "Invalid task number. Please select a valid task number from the list."
            
            # If none of the above conditions matched, process as normal
            else:
                # Analyze the user's message to determine intent
                actions_taken = []
                ai_response = ""

                # Simple keyword-based intent detection (would be replaced with proper NLP in production)
                message_lower = chat_request.message.lower()

                if any(word in message_lower for word in ["add", "create", "new task", "make"]):
                    # Extract task title from message (simple extraction)
                    task_title = chat_request.message.replace("Add", "").replace("add", "").replace("Create", "").replace("create", "").strip()
                    if task_title.startswith("a task to ") or task_title.startswith("a task that "):
                        task_title = task_title[10:].strip()
                    elif task_title.startswith("to "):
                        task_title = task_title[3:].strip()

                    # Call the add_task_tool
                    result = await ai_service.add_task_tool(task_title, current_user, session, None)
                    if result["success"]:
                        ai_response = f"Task added: {result['message']}"
                        actions_taken = [{
                            "action": "task_created",
                            "task_id": result["task_id"],
                            "details": result["message"]
                        }]
                    else:
                        ai_response = f"Failed to add task: {result['message']}"

                elif any(word in message_lower for word in ["list", "show", "display", "my tasks", "get"]):
                    # Call the list_tasks_tool
                    result = await ai_service.list_tasks_tool(current_user, session)
                    if result["success"]:
                        task_list = [f"- {task['title']} ({'✓' if task['completed'] else '○'})" for task in result["tasks"]]
                        ai_response = f"Here are your tasks:\n" + "\n".join(task_list) if task_list else "You have no tasks."
                        actions_taken = [{
                            "action": "tasks_listed",
                            "count": result["count"],
                            "details": f"Listed {result['count']} tasks"
                        }]
                    else:
                        ai_response = f"Failed to list tasks: {result['message']}"

                elif any(word in message_lower for word in ["update", "change", "modify"]):
                    # Simple implementation - would need more sophisticated parsing in production
                    ai_response = "Task update functionality would be implemented here with proper NLP parsing."

                elif any(word in message_lower for word in ["delete", "remove"]):
                    # Extract task ID from message if specified
                    import re
                    task_id_match = re.search(r'\b(\d+)\b', chat_request.message)
                    if task_id_match:
                        task_id = int(task_id_match.group(1))
                        # Call the delete_task_tool
                        result = await ai_service.delete_task_tool(task_id, current_user, session)
                        if result["success"]:
                            ai_response = result["message"]
                            actions_taken = [{
                                "action": "task_deleted",
                                "task_id": task_id,
                                "details": result["message"]
                            }]
                        else:
                            ai_response = f"Failed to delete task: {result['message']}"
                    else:
                        ai_response = "Please specify a task ID to delete. Example: 'Delete task 1' or 'Remove task 5'."

                elif any(word in message_lower for word in ["complete", "done", "finish", "mark as"]):
                    # Extract task ID from message if specified
                    import re
                    task_id_match = re.search(r'\b(\d+)\b', chat_request.message)
                    if task_id_match:
                        task_id = int(task_id_match.group(1))
                        # Call the complete_task_tool
                        result = await ai_service.complete_task_tool(task_id, current_user, session)
                        if result["success"]:
                            status_text = "completed" if result["completed"] else "marked as incomplete"
                            ai_response = result["message"]
                            actions_taken = [{
                                "action": "task_completed",
                                "task_id": task_id,
                                "details": f"Task {status_text}"
                            }]
                        else:
                            ai_response = f"Failed to complete task: {result['message']}"
                    else:
                        ai_response = "Please specify a task ID to mark as complete. Example: 'Complete task 1' or 'Mark task 3 as done'."

                else:
                    # Check if the user is initiating a conversation or asking for help
                    message_lower = chat_request.message.lower()
                    if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "chat", "help", "start"]):
                        ai_response = "Hello! I'm your AI Task Assistant. How can I help you today?\n\n" \
                                     "Select an option:\n" \
                                     "1. Add task\n" \
                                     "2. List tasks\n" \
                                     "3. Mark as complete\n" \
                                     "4. Delete task\n\n" \
                                     "Enter the number of your choice (1-4)"
                    # Handle numeric inputs for menu selection
                    elif message_lower == "1":
                        ai_response = "Add your task now. Please provide the task title:"
                    elif message_lower == "2":
                        # Call the list_tasks_tool
                        result = await ai_service.list_tasks_tool(current_user, session)
                        if result["success"]:
                            if result["tasks"]:
                                task_list = [f"{i+1}. {task['title']} ({'✓' if task['completed'] else '○'})" for i, task in enumerate(result["tasks"])]
                                ai_response = "Your tasks:\n" + "\n".join(task_list)
                            else:
                                ai_response = "You have no tasks."
                        else:
                            ai_response = f"Failed to list tasks: {result['message']}"
                    elif message_lower == "3":
                        # First list tasks so user knows which ones to complete
                        result = await ai_service.list_tasks_tool(current_user, session)
                        if result["success"]:
                            if result["tasks"]:
                                task_list = [f"{task['id']}. {task['title']} ({'✓' if task['completed'] else '○'})" for task in result["tasks"]]
                                ai_response = "Which task would you like to mark as complete? Select the task number:\n" + "\n".join(task_list) + "\n\nReply with the task number (e.g., '1' to complete the first task)"
                            else:
                                ai_response = "You have no tasks to complete."
                        else:
                            ai_response = f"Failed to list tasks: {result['message']}"
                    elif message_lower == "4":
                        # First list tasks so user knows which ones to delete
                        result = await ai_service.list_tasks_tool(current_user, session)
                        if result["success"]:
                            if result["tasks"]:
                                task_list = [f"{task['id']}. {task['title']} ({'✓' if task['completed'] else '○'})" for task in result["tasks"]]
                                ai_response = "Which task would you like to delete? Select the task number:\n" + "\n".join(task_list) + "\n\nReply with the task number (e.g., '1' to delete the first task)"
                            else:
                                ai_response = "You have no tasks to delete."
                        else:
                            ai_response = f"Failed to list tasks: {result['message']}"
                    else:
                        # Default response for unrecognized commands
                        ai_response = f"I received your message: '{chat_request.message}'. I can help you manage your tasks. Type 'hello' for options."
        else:
            # This is the first message in the conversation
            # Analyze the user's message to determine intent
            actions_taken = []
            ai_response = ""

            # Simple keyword-based intent detection (would be replaced with proper NLP in production)
            message_lower = chat_request.message.lower()

            if any(word in message_lower for word in ["add", "create", "new task", "make"]):
                # Extract task title from message (simple extraction)
                task_title = chat_request.message.replace("Add", "").replace("add", "").replace("Create", "").replace("create", "").strip()
                if task_title.startswith("a task to ") or task_title.startswith("a task that "):
                    task_title = task_title[10:].strip()
                elif task_title.startswith("to "):
                    task_title = task_title[3:].strip()

                # Call the add_task_tool
                result = await ai_service.add_task_tool(task_title, current_user, session, None)
                if result["success"]:
                    ai_response = f"Task added: {result['message']}"
                    actions_taken = [{
                        "action": "task_created",
                        "task_id": result["task_id"],
                        "details": result["message"]
                    }]
                else:
                    ai_response = f"Failed to add task: {result['message']}"

            elif any(word in message_lower for word in ["list", "show", "display", "my tasks", "get"]):
                # Call the list_tasks_tool
                result = await ai_service.list_tasks_tool(current_user, session)
                if result["success"]:
                    task_list = [f"- {task['title']} ({'✓' if task['completed'] else '○'})" for task in result["tasks"]]
                    ai_response = f"Here are your tasks:\n" + "\n".join(task_list) if task_list else "You have no tasks."
                    actions_taken = [{
                        "action": "tasks_listed",
                        "count": result["count"],
                        "details": f"Listed {result['count']} tasks"
                    }]
                else:
                    ai_response = f"Failed to list tasks: {result['message']}"

            elif any(word in message_lower for word in ["update", "change", "modify"]):
                # Simple implementation - would need more sophisticated parsing in production
                ai_response = "Task update functionality would be implemented here with proper NLP parsing."

            elif any(word in message_lower for word in ["delete", "remove"]):
                # Extract task ID from message if specified
                import re
                task_id_match = re.search(r'\b(\d+)\b', chat_request.message)
                if task_id_match:
                    task_id = int(task_id_match.group(1))
                    # Call the delete_task_tool
                    result = await ai_service.delete_task_tool(task_id, current_user, session)
                    if result["success"]:
                        ai_response = result["message"]
                        actions_taken = [{
                            "action": "task_deleted",
                            "task_id": task_id,
                            "details": result["message"]
                        }]
                    else:
                        ai_response = f"Failed to delete task: {result['message']}"
                else:
                    ai_response = "Please specify a task ID to delete. Example: 'Delete task 1' or 'Remove task 5'."

            elif any(word in message_lower for word in ["complete", "done", "finish", "mark as"]):
                # Extract task ID from message if specified
                import re
                task_id_match = re.search(r'\b(\d+)\b', chat_request.message)
                if task_id_match:
                    task_id = int(task_id_match.group(1))
                    # Call the complete_task_tool
                    result = await ai_service.complete_task_tool(task_id, current_user, session)
                    if result["success"]:
                        status_text = "completed" if result["completed"] else "marked as incomplete"
                        ai_response = result["message"]
                        actions_taken = [{
                            "action": "task_completed",
                            "task_id": task_id,
                            "details": f"Task {status_text}"
                        }]
                    else:
                        ai_response = f"Failed to complete task: {result['message']}"
                else:
                    ai_response = "Please specify a task ID to mark as complete. Example: 'Complete task 1' or 'Mark task 3 as done'."

            else:
                # Check if the user is initiating a conversation or asking for help
                message_lower = chat_request.message.lower()
                if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "chat", "help", "start"]):
                    ai_response = "Hello! I'm your AI Task Assistant. How can I help you today?\n\n" \
                                 "Select an option:\n" \
                                 "1. Add task\n" \
                                 "2. List tasks\n" \
                                 "3. Mark as complete\n" \
                                 "4. Delete task\n\n" \
                                 "Enter the number of your choice (1-4)"
                # Handle numeric inputs for menu selection
                elif message_lower == "1":
                    ai_response = "Add your task now. Please provide the task title.\n\nExample: 'Buy groceries' or 'Finish project report'"
                elif message_lower == "2":
                    # Call the list_tasks_tool
                    result = await ai_service.list_tasks_tool(current_user, session)
                    if result["success"]:
                        if result["tasks"]:
                            task_list = [f"{i+1}. {task['title']} ({'✓' if task['completed'] else '○'})" for i, task in enumerate(result["tasks"])]
                            ai_response = "Your tasks:\n" + "\n".join(task_list)
                        else:
                            ai_response = "You have no tasks."
                    else:
                        ai_response = f"Failed to list tasks: {result['message']}"
                elif message_lower == "3":
                    # First list tasks so user knows which ones to complete
                    result = await ai_service.list_tasks_tool(current_user, session)
                    if result["success"]:
                        if result["tasks"]:
                            task_list = [f"{task['id']}. {task['title']} ({'✓' if task['completed'] else '○'})" for task in result["tasks"]]
                            ai_response = "Which task would you like to mark as complete? Select the task number:\n" + "\n".join(task_list) + "\n\nReply with the task number (e.g., '1' to complete the first task)\n\nExample: Reply with '1' to mark the first task as complete"
                        else:
                            ai_response = "You have no tasks to complete."
                    else:
                        ai_response = f"Failed to list tasks: {result['message']}"
                elif message_lower == "4":
                    # First list tasks so user knows which ones to delete
                    result = await ai_service.list_tasks_tool(current_user, session)
                    if result["success"]:
                        if result["tasks"]:
                            task_list = [f"{task['id']}. {task['title']} ({'✓' if task['completed'] else '○'})" for task in result["tasks"]]
                            ai_response = "Which task would you like to delete? Select the task number:\n" + "\n".join(task_list) + "\n\nReply with the task number (e.g., '1' to delete the first task)\n\nExample: Reply with '1' to delete the first task"
                        else:
                            ai_response = "You have no tasks to delete."
                    else:
                        ai_response = f"Failed to list tasks: {result['message']}"
                else:
                    # Default response for unrecognized commands
                    ai_response = f"I received your message: '{chat_request.message}'. I can help you manage your tasks. Type 'hello' for options."
        
        # Save AI response to conversation
        ai_message = MessageCreate(
            role=MessageRole.ASSISTANT,
            content=ai_response,
            conversation_id=conversation.id
        )
        await ConversationService.add_message_to_conversation(session, ai_message)
        
        return {
            "success": True,
            "data": {
                "response": ai_response,
                "conversation_id": conversation.id,
                "actions_taken": actions_taken
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}"
        )


@router.get("/{user_id}/conversations")
async def get_user_conversations(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve list of conversation summaries for the authenticated user.
    
    Args:
        user_id: ID of the authenticated user
        session: Async database session
        
    Returns:
        Dictionary containing list of conversations
    """
    try:
        conversations = await ConversationService.get_conversations_by_user_id(session, user_id)
        
        return {
            "success": True,
            "data": {
                "conversations": [conv.model_dump() for conv in conversations],
                "total": len(conversations)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve conversations: {str(e)}"
        )


@router.get("/{user_id}/conversations/{conversation_id}")
async def get_conversation_history(
    user_id: int,
    conversation_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve full conversation history with messages.
    
    Args:
        user_id: ID of the authenticated user
        conversation_id: ID of the conversation to retrieve
        session: Async database session
        
    Returns:
        Dictionary containing conversation details with messages
    """
    try:
        conversation = await ConversationService.get_conversation_by_id(session, conversation_id, user_id)
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        messages = await ConversationService.get_messages_by_conversation_id(session, conversation_id)
        
        return {
            "success": True,
            "data": {
                "conversation": {
                    "id": conversation.id,
                    "title": conversation.title,
                    "created_at": conversation.created_at,
                    "updated_at": conversation.updated_at,
                    "messages": [msg.model_dump() for msg in messages]
                }
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve conversation history: {str(e)}"
        )