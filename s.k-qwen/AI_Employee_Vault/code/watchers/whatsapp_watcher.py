#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WhatsApp Watcher - Monitors WhatsApp Web for new messages.

Uses Playwright to automate WhatsApp Web and detect unread messages
containing important keywords. Creates action files for AI processing.

Usage:
    python whatsapp_watcher.py <vault_path> [check_interval_seconds]

Example:
    python whatsapp_watcher.py ../ 30

Prerequisites:
    1. Install Playwright: pip install playwright
    2. Install browsers: playwright install
    3. First run will open browser for QR code scan
    4. Session will be saved for subsequent runs

⚠️ WARNING: Be aware of WhatsApp's Terms of Service when using automation.

Features:
    - Monitors WhatsApp Web for unread messages
    - Filters by keywords (urgent, invoice, payment, help, etc.)
    - Creates markdown action files with message metadata
    - Persistent session (scan QR code only once)
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from base_watcher import BaseWatcher

# Playwright dependencies
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not installed. Run: pip install playwright && playwright install")


class WhatsAppWatcher(BaseWatcher):
    """
    WhatsApp Web Watcher using Playwright automation.
    """
    
    # Keywords that indicate important messages
    KEYWORDS = ['urgent', 'asap', 'invoice', 'payment', 'help', 
                'important', 'deadline', 'call', 'meeting', 'money']
    
    # WhatsApp Web URL
    WHATSAPP_WEB_URL = 'https://web.whatsapp.com'
    
    def __init__(self, vault_path: str, session_path: str = None,
                 check_interval: int = 30):
        """
        Initialize the WhatsApp watcher.
        
        Args:
            vault_path: Path to the Obsidian vault
            session_path: Path to store browser session data
            check_interval: How often to check for new messages (seconds)
        """
        super().__init__(vault_path, check_interval)
        
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright not installed")
        
        # Set session path
        self.session_path = Path(session_path) if session_path else Path(__file__).parent / 'whatsapp_session'
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        # Track processed messages
        self.processed_messages = set()
        
        # Load previously processed messages from cache
        self._load_cache()
    
    def _load_cache(self):
        """Load cached processed message IDs."""
        cache_file = Path(__file__).parent / 'whatsapp_cache.json'
        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text())
                self.processed_messages = set(data.get('processed_messages', []))
            except:
                pass
    
    def _save_cache(self):
        """Save processed message IDs to cache file."""
        cache_file = Path(__file__).parent / 'whatsapp_cache.json'
        try:
            msgs_list = list(self.processed_messages)[-500:]
            cache_file.write_text(json.dumps({'processed_messages': msgs_list}))
        except:
            pass
    
    def check_for_updates(self) -> list:
        """Check WhatsApp Web for new important messages."""
        new_messages = []
        
        try:
            with sync_playwright() as p:
                # Launch browser with persistent context
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    args=[
                        '--disable-gpu',
                        '--disable-dev-shm-usage',
                        '--no-sandbox'
                    ]
                )
                
                page = browser.pages[0] if browser.pages else browser.new_page()
                
                # Navigate to WhatsApp Web
                page.goto(self.WHATSAPP_WEB_URL)
                
                try:
                    # Wait for chat list to load
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                    time.sleep(3)  # Let content load
                    
                    # Find all chat items with unread indicator
                    unread_chats = page.query_selector_all('[aria-label*="unread"]')
                    
                    for chat in unread_chats:
                        try:
                            chat_text = chat.inner_text()
                            chat_text_lower = chat_text.lower()
                            
                            # Check if contains important keywords
                            if any(kw in chat_text_lower for kw in self.KEYWORDS):
                                chat_name = self._extract_chat_name(chat_text)
                                msg_id = f"{chat_name}_{datetime.now().strftime('%Y%m%d_%H')}"
                                
                                if msg_id not in self.processed_messages:
                                    new_messages.append({
                                        'id': msg_id,
                                        'chat': chat_name,
                                        'text': chat_text,
                                        'timestamp': datetime.now().isoformat(),
                                        'keywords_found': [kw for kw in self.KEYWORDS if kw in chat_text_lower]
                                    })
                                    self.processed_messages.add(msg_id)
                        except Exception as e:
                            self.logger.debug(f"Error processing chat: {e}")
                            continue
                    
                    if new_messages:
                        self._save_cache()
                    
                except PlaywrightTimeout:
                    self.logger.warning("Timeout waiting for WhatsApp chat list")
                except Exception as e:
                    self.logger.error(f"Error interacting with WhatsApp: {e}")
                finally:
                    browser.close()
                    
        except Exception as e:
            self.logger.error(f"Error in WhatsApp watcher: {e}")
        
        return new_messages
    
    def _extract_chat_name(self, chat_text: str) -> str:
        """Extract chat name/number from chat text."""
        lines = chat_text.strip().split('\n')
        if lines:
            return lines[0].strip()[:50]
        return "Unknown"
    
    def create_action_file(self, item: dict) -> Path:
        """Create a markdown action file for the WhatsApp message."""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        chat_safe = self.sanitize_filename(item['chat'], 20)
        filename = f"WHATSAPP_{timestamp}_{chat_safe}.md"
        filepath = self.needs_action / filename
        
        priority = 'high' if 'urgent' in item['keywords_found'] or 'asap' in item['keywords_found'] else 'normal'
        
        content = f'''---
type: whatsapp_message
from: {item['chat']}
received: {item['timestamp']}
priority: {priority}
status: pending
keywords: {', '.join(item['keywords_found'])}
---

# WhatsApp Message Received

## Message Information

- **From:** {item['chat']}
- **Received:** {item['timestamp']}
- **Priority:** {priority}
- **Keywords:** {', '.join(item['keywords_found'])}

## Message Content

{item['text']}

## Suggested Actions

- [ ] Open WhatsApp and read full message
- [ ] Reply to sender
- [ ] Take appropriate action
- [ ] Mark as read in WhatsApp
- [ ] Archive after processing

## Notes

*Add any notes or context for processing this message.*

---
*Automatically imported by WhatsApp Watcher*
'''
        
        filepath.write_text(content)
        self.logger.info(f"Created action file: {filename}")
        return filepath
    
    def run(self):
        """Main run loop with initial authentication."""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Session path: {self.session_path}')
        self.logger.info('First run: Scan QR code with WhatsApp mobile app')
        
        # First run - authenticate
        self._initial_auth()
        
        # Start normal monitoring
        super().run()
    
    def _initial_auth(self):
        """Perform initial authentication via QR code."""
        self.logger.info('Opening browser for QR code authentication...')
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,
                    args=['--disable-gpu', '--no-sandbox']
                )
                
                page = browser.pages[0] if browser.pages else browser.new_page()
                page.goto(self.WHATSAPP_WEB_URL)
                
                self.logger.info('Scan QR code with your WhatsApp mobile app')
                self.logger.info('Waiting 60 seconds for authentication...')
                
                try:
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
                    self.logger.info('Authentication successful!')
                except PlaywrightTimeout:
                    self.logger.warning('QR code scan timeout. Will retry on next run.')
                
                browser.close()
                
        except Exception as e:
            self.logger.error(f'Authentication error: {e}')


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python whatsapp_watcher.py <vault_path> [check_interval_seconds]")
        print("\n⚠️ WARNING: Be aware of WhatsApp's Terms of Service.")
        sys.exit(1)
    
    vault_path = sys.argv[1]
    check_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    
    if not Path(vault_path).exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    try:
        watcher = WhatsAppWatcher(vault_path, check_interval=check_interval)
        watcher.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
