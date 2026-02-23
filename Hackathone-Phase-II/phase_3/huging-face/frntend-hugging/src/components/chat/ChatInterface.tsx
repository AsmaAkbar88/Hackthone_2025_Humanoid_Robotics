import React, { useState, useRef, useEffect } from 'react';
import useChat from '../../hooks/useChat';
import { useTasks } from '@/hooks/useTasks';

interface MessageAction {
  action: string;
  details?: string;
  params?: any;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  actionsTaken?: MessageAction[];
  timestamp?: string;
}

interface ChatInterfaceProps {
  conversationId?: string | null;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ conversationId = null }) => {
  const { messages, isLoading, error, sendMessage } = useChat();
  const { 
    createTask: createGlobalTask, 
    fetchTasks, 
    state: tasksState,
    updateTask,
    deleteTask
  } = useTasks(); // Access the global task context
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Send the message
    const response = await sendMessage(inputValue, conversationId);

    // After sending the message, check if it triggered any task operations
    // and update the global task state immediately
    if (response && response.success && response.actions_taken && Array.isArray(response.actions_taken)) {
      // Check if any of the actions were task-related
      const taskActions = response.actions_taken.filter(action =>
        action && action.action && ['task_created', 'task_completed', 'task_updated', 'task_deleted'].includes(action.action)
      );

      if (taskActions.length > 0) {
        // Refresh all tasks to sync with backend
        // This ensures that the dashboard gets updated with the new task
        await fetchTasks();
      }
    }

    setInputValue(''); // Clear the input after sending
  };

  // Scroll to bottom of messages when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-md p-4">
      {/* Chat header */}
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-gray-800">AI Task Assistant</h2>
        <p className="text-sm text-gray-600">Manage your tasks with natural language</p>
      </div>

      {/* Messages container */}
      <div className="flex-grow overflow-y-auto max-h-[400px] mb-4 border border-gray-200 rounded p-3 bg-gray-50">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            <p>Start a conversation to manage your tasks...</p>
          </div>
        ) : (
          <div className="space-y-3">
            {messages.map((message) => (
              <div
                key={message.id}
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
                    <div className="mt-2 text-xs opacity-80">
                      Actions taken: {message.actionsTaken.map(action => action.details).join(', ')}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-200 text-gray-800 rounded-lg p-3 max-w-[80%]">
                  <div className="font-medium text-xs mb-1">AI Assistant</div>
                  <div className="text-sm">Thinking...</div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Error message */}
      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
          Error: {error}
        </div>
      )}

      {/* Input form */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your task command (e.g., 'Add a task to buy groceries')"
          className="flex-grow border border-gray-300 rounded-l-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isLoading}
        />
        <button
          type="submit"
          className={`px-4 py-3 rounded-r-lg font-medium ${
            isLoading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-500 hover:bg-blue-600 text-white'
          }`}
          disabled={isLoading || !inputValue.trim()}
        >
          Send
        </button>
      </form>

      {/* Example commands */}
      <div className="mt-3 text-xs text-gray-500">
        <p>Examples: "Add a task to buy groceries", "Show me my tasks", "Mark task 1 as complete"</p>
      </div>
    </div>
  );
};

export default ChatInterface;