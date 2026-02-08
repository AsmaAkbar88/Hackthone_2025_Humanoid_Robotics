"""
Conversation Service for the Todo Backend API.

Handles all conversation-related operations including creation, retrieval, and message management.
"""
from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate


class ConversationService:
    """
    Service class to handle conversation operations.
    """
    
    @staticmethod
    async def create_conversation(
        session: AsyncSession, 
        conversation: ConversationCreate
    ) -> Conversation:
        """
        Create a new conversation.
        
        Args:
            session: Database session
            conversation: Conversation data to create
            
        Returns:
            Created Conversation object
        """
        db_conversation = Conversation.model_validate(conversation)
        session.add(db_conversation)
        await session.commit()
        await session.refresh(db_conversation)
        return db_conversation
    
    @staticmethod
    async def get_conversation_by_id(
        session: AsyncSession, 
        conversation_id: int, 
        user_id: int
    ) -> Optional[Conversation]:
        """
        Get a conversation by its ID for a specific user.
        
        Args:
            session: Database session
            conversation_id: ID of the conversation to retrieve
            user_id: ID of the user who owns the conversation
            
        Returns:
            Conversation object if found, None otherwise
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await session.execute(statement)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_conversations_by_user_id(
        session: AsyncSession, 
        user_id: int
    ) -> List[Conversation]:
        """
        Get all conversations for a specific user.
        
        Args:
            session: Database session
            user_id: ID of the user whose conversations to retrieve
            
        Returns:
            List of Conversation objects
        """
        statement = select(Conversation).where(Conversation.user_id == user_id)
        result = await session.execute(statement)
        return result.scalars().all()
    
    @staticmethod
    async def add_message_to_conversation(
        session: AsyncSession, 
        message: MessageCreate
    ) -> Message:
        """
        Add a message to a conversation.
        
        Args:
            session: Database session
            message: Message data to add
            
        Returns:
            Created Message object
        """
        db_message = Message.model_validate(message)
        session.add(db_message)
        await session.commit()
        await session.refresh(db_message)
        return db_message
    
    @staticmethod
    async def get_messages_by_conversation_id(
        session: AsyncSession, 
        conversation_id: int
    ) -> List[Message]:
        """
        Get all messages for a specific conversation.
        
        Args:
            session: Database session
            conversation_id: ID of the conversation whose messages to retrieve
            
        Returns:
            List of Message objects
        """
        statement = select(Message).where(Message.conversation_id == conversation_id)
        result = await session.execute(statement)
        return result.scalars().all()
    
    @staticmethod
    async def delete_conversation(
        session: AsyncSession, 
        conversation_id: int, 
        user_id: int
    ) -> bool:
        """
        Delete a conversation by its ID for a specific user.
        
        Args:
            session: Database session
            conversation_id: ID of the conversation to delete
            user_id: ID of the user who owns the conversation
            
        Returns:
            True if conversation was deleted, False otherwise
        """
        conversation = await ConversationService.get_conversation_by_id(
            session, conversation_id, user_id
        )
        
        if not conversation:
            return False
        
        await session.delete(conversation)
        await session.commit()
        return True