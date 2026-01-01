/**
 * Docusaurus Client Module Entry Point for Chatbot UI
 * Lazily loads and renders the ChatWidget component
 */

import React, { useEffect } from 'react';
import ReactDOM from 'react-dom/client';

function ChatbotRoot() {
  useEffect(() => {
    // Lazy load the ChatWidget component
    import('./components/ChatWidget').then(({ default: ChatWidget }) => {
      // Create container element if it doesn't exist
      let container = document.getElementById('chatbot-widget-container');
      if (!container) {
        container = document.createElement('div');
        container.id = 'chatbot-widget-container';
        document.body.appendChild(container);
      }

      // Create root and render ChatWidget
      const root = ReactDOM.createRoot(container);
      root.render(<ChatWidget />);
    }).catch((error) => {
      console.error('Failed to load chatbot widget:', error);
    });
  }, []);

  // This component doesn't render anything itself
  return null;
}

// Export for Docusaurus client module
export default ChatbotRoot;
