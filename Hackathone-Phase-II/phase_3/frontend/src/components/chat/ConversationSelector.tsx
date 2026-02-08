import React from 'react';

const ConversationSelector = ({ conversations, onSelectConversation, onCreateNew }) => {
  return (
    <div className="border border-gray-200 rounded-lg p-3 bg-gray-50">
      <div className="flex justify-between items-center mb-3">
        <h3 className="font-medium text-gray-700">Conversations</h3>
        <button
          onClick={onCreateNew}
          className="text-sm bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600"
        >
          New
        </button>
      </div>
      
      {conversations.length === 0 ? (
        <p className="text-sm text-gray-500">No conversations yet</p>
      ) : (
        <ul className="space-y-2 max-h-60 overflow-y-auto">
          {conversations.map((conversation) => (
            <li key={conversation.id}>
              <button
                onClick={() => onSelectConversation(conversation.id)}
                className="w-full text-left p-2 rounded hover:bg-gray-100 text-sm truncate"
                title={conversation.title}
              >
                <div className="font-medium">{conversation.title}</div>
                <div className="text-xs text-gray-500">
                  {new Date(conversation.updated_at).toLocaleDateString()}
                </div>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ConversationSelector;