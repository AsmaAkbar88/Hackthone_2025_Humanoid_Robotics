/**
 * Docusaurus Client Configuration for Chatbot
 * Injects chatbot UI into all pages
 */

export default function injectChatbot(config) {
  return {
    name: 'inject-chatbot',
    injectHtmlTags: [
      {
        tagName: 'div',
        innerHTML: '<div id="chatbot-widget-root"></div>',
      },
    ],
  };
}

export default function wrapRootComponent(OriginalRoot, props) {
  return function ChatbotRootWrapper({ children }) {
    // Dynamically import and render ChatWidget
    React.useEffect(() => {
      import('../backend/ui_chatbot/components/ChatWidget').then(({ default: ChatWidget }) => {
        const root = document.getElementById('chatbot-widget-root');
        if (root && !root.hasChildNodes()) {
          const { createRoot } = require('react-dom/client');
          const rootInstance = createRoot(root);
          rootInstance.render(<ChatWidget />);
        }
      });
    }, []);

    return <OriginalRoot {...props} />;
  };
}
