import React from 'react';

interface ActionTaken {
  action: string;
  details?: string;
  [key: string]: any; // Allow additional properties
}

interface ChatMessage {
  id: string | number;
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  actionsTaken?: ActionTaken[];
}

interface ChatHistoryProps {
  messages: ChatMessage[];
  isLoading?: boolean;
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ messages, isLoading = false }) => {
  if (messages.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500 p-4">
        <p>No conversation history available</p>
      </div>
    );
  }

  return (
    <div className="overflow-y-auto max-h-[300px] mb-4">
      <div className="space-y-3">
        {messages.map((message) => (
          <div
            key={message.id || message.timestamp}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                message.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              <div className="font-medium text-xs mb-1">
                {message.role === 'user' ? 'You' : 'AI Assistant'}
              </div>
              <div className="text-sm">{message.content}</div>
              {message.actionsTaken && message.actionsTaken.length > 0 && (
                <div className="mt-1 text-xs opacity-80">
                  Actions: {message.actionsTaken.map(action => action.action).join(', ')}
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 text-gray-800 rounded-lg p-3 max-w-[80%]">
              <div className="font-medium text-xs mb-1">AI Assistant</div>
              <div className="text-sm">Loading...</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatHistory;