import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

export default function onClientEntry() {
  const isClient = ExecutionEnvironment.canUseDOM;

  if (!isClient) {
    return null;
  }

  // Load and render chatbot widget on client
  import('./components/chatbot/ChatWidget').then(({ default: ChatWidget }) => {
    // Create root container if it doesn't exist
    let root = document.getElementById('chatbot-widget-root');
    if (!root) {
      root = document.createElement('div');
      root.id = 'chatbot-widget-root';
      document.body.appendChild(root);
    }

    // Wait for React to be available and render widget
    const renderWidget = () => {
      if (typeof React !== 'undefined' && typeof ReactDOM !== 'undefined') {
        const { createRoot } = require('react-dom/client');
        const rootInstance = createRoot(root);
        rootInstance.render(<ChatWidget />);
        console.log('Chatbot widget injected successfully');
      }
    };

    // Try to render immediately if React is available
    if (typeof React !== 'undefined' && typeof ReactDOM !== 'undefined') {
      renderWidget();
    } else {
      // Wait for React to load
      window.addEventListener('load', renderWidget);
    }
  }).catch((error) => {
    console.error('Failed to load chatbot widget:', error);
  });
}
