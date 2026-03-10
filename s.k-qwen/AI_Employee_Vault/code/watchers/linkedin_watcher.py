#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Watcher - Monitors LinkedIn for notifications and messages.

Uses Playwright to automate LinkedIn and detect important notifications
like connection requests, messages, and engagement on posts.

Usage:
    python linkedin_watcher.py <vault_path> [check_interval_seconds]

Example:
    python linkedin_watcher.py ../ 300

Prerequisites:
    1. Install Playwright: pip install playwright
    2. Install browsers: playwright install
    3. First run will open browser for login
    4. Session will be saved for subsequent runs

⚠️ WARNING: Be aware of LinkedIn's Terms of Service when using automation.

Features:
    - Monitors LinkedIn for notifications
    - Detects messages, connection requests, post engagement
    - Creates markdown action files for AI processing
    - Persistent session (login once)
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


class LinkedInWatcher(BaseWatcher):
    """
    LinkedIn Watcher using Playwright automation.
    """
    
    # Notification types to monitor
    NOTIFICATION_TYPES = [
        'message', 'connection', 'job', 'post', 'comment', 'like'
    ]
    
    # Keywords for business opportunities
    BUSINESS_KEYWORDS = [
        'hiring', 'opportunity', 'project', 'freelance', 'contract',
        'proposal', 'partnership', 'collaboration', 'investment'
    ]
    
    # LinkedIn URLs
    LINKEDIN_URL = 'https://www.linkedin.com'
    NOTIFICATIONS_URL = 'https://www.linkedin.com/notifications'
    MESSAGING_URL = 'https://www.linkedin.com/messaging'
    
    def __init__(self, vault_path: str, session_path: str = None,
                 check_interval: int = 300):
        """
        Initialize the LinkedIn watcher.
        
        Args:
            vault_path: Path to the Obsidian vault
            session_path: Path to store browser session data
            check_interval: How often to check (seconds, default: 5 min)
        """
        super().__init__(vault_path, check_interval)
        
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright not installed")
        
        # Set session path
        self.session_path = Path(session_path) if session_path else Path(__file__).parent / 'linkedin_session'
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        # Track processed notifications
        self.processed_notifications = set()
        
        # Load cache
        self._load_cache()
    
    def _load_cache(self):
        """Load cached processed notification IDs."""
        cache_file = Path(__file__).parent / 'linkedin_cache.json'
        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text())
                self.processed_notifications = set(data.get('processed_ids', []))
            except:
                pass
    
    def _save_cache(self):
        """Save processed notification IDs."""
        cache_file = Path(__file__).parent / 'linkedin_cache.json'
        try:
            ids_list = list(self.processed_notifications)[-500:]
            cache_file.write_text(json.dumps({'processed_ids': ids_list}))
        except:
            pass
    
    def check_for_updates(self) -> list:
        """Check LinkedIn for new notifications and messages."""
        new_items = []
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    args=['--disable-gpu', '--disable-dev-shm-usage', '--no-sandbox']
                )
                
                page = browser.pages[0] if browser.pages else browser.new_page()
                
                # Navigate to LinkedIn
                page.goto(self.LINKEDIN_URL)
                
                try:
                    # Wait for page to load
                    page.wait_for_load_state('networkidle', timeout=30000)
                    time.sleep(5)
                    
                    # Check if logged in by looking for notifications icon
                    is_logged_in = page.query_selector('[aria-label="Notifications"]') is not None
                    
                    if not is_logged_in:
                        self.logger.warning('Not logged in. Please authenticate manually.')
                        browser.close()
                        return []
                    
                    # Navigate to notifications
                    page.goto(self.NOTIFICATIONS_URL)
                    time.sleep(3)
                    
                    # Get notifications
                    notifications = self._extract_notifications(page)
                    
                    for notif in notifications:
                        notif_id = f"{notif['type']}_{notif.get('actor', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H')}"
                        
                        if notif_id not in self.processed_notifications:
                            # Check if it's business-related
                            if self._is_business_relevant(notif):
                                new_items.append(notif)
                                self.processed_notifications.add(notif_id)
                    
                    if new_items:
                        self._save_cache()
                    
                except PlaywrightTimeout:
                    self.logger.warning("Timeout waiting for LinkedIn page")
                except Exception as e:
                    self.logger.error(f"Error on LinkedIn: {e}")
                finally:
                    browser.close()
                    
        except Exception as e:
            self.logger.error(f"Error in LinkedIn watcher: {e}")
        
        return new_items
    
    def _extract_notifications(self, page) -> List[Dict]:
        """Extract notifications from the page."""
        notifications = []
        
        try:
            # Try to find notification elements
            notif_elements = page.query_selector_all('div.notification-item')
            
            for elem in notif_elements[:10]:  # Limit to 10 notifications
                try:
                    text = elem.inner_text()
                    
                    notifications.append({
                        'type': self._detect_notification_type(text),
                        'text': text[:500],
                        'actor': self._extract_actor(text),
                        'timestamp': datetime.now().isoformat(),
                        'url': self.LINKEDIN_URL
                    })
                except:
                    continue
                    
        except Exception as e:
            self.logger.debug(f"Could not extract notifications: {e}")
            
            # Fallback: check for messaging
            try:
                page.goto(self.MESSAGING_URL)
                time.sleep(3)
                
                # Look for unread messages
                unread = page.query_selector_all('[aria-label*="unread"]')
                
                for msg in unread:
                    text = msg.inner_text()
                    notifications.append({
                        'type': 'message',
                        'text': text[:500],
                        'actor': 'LinkedIn Message',
                        'timestamp': datetime.now().isoformat(),
                        'url': self.MESSAGING_URL
                    })
            except:
                pass
        
        return notifications
    
    def _detect_notification_type(self, text: str) -> str:
        """Detect the type of notification from text."""
        text_lower = text.lower()
        
        if 'message' in text_lower or 'messaged you' in text_lower:
            return 'message'
        elif 'connection' in text_lower or 'wants to connect' in text_lower:
            return 'connection'
        elif 'job' in text_lower:
            return 'job'
        elif 'comment' in text_lower or 'commented on' in text_lower:
            return 'comment'
        elif 'like' in text_lower or 'reacted to' in text_lower:
            return 'like'
        elif 'post' in text_lower:
            return 'post'
        else:
            return 'other'
    
    def _extract_actor(self, text: str) -> str:
        """Extract the actor name from notification text."""
        # First line usually contains the name
        lines = text.strip().split('\n')
        if lines:
            return lines[0].strip()[:50]
        return "Unknown"
    
    def _is_business_relevant(self, notif: Dict) -> bool:
        """Check if notification is business-relevant."""
        text = notif['text'].lower()
        
        # Business keywords
        if any(kw in text for kw in self.BUSINESS_KEYWORDS):
            return True
        
        # Important notification types
        if notif['type'] in ['message', 'connection']:
            return True
        
        return False
    
    def create_action_file(self, item: dict) -> Path:
        """Create a markdown action file for the LinkedIn notification."""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        notif_type = item['type']
        filename = f"LINKEDIN_{timestamp}_{notif_type}.md"
        filepath = self.needs_action / filename
        
        priority = 'high' if notif_type == 'message' else 'normal'
        
        content = f'''---
type: linkedin_{notif_type}
notification_type: {notif_type}
received: {item['timestamp']}
priority: {priority}
status: pending
url: {item['url']}
---

# LinkedIn Notification

## Notification Information

- **Type:** {notif_type}
- **From:** {item['actor']}
- **Received:** {item['timestamp']}
- **Priority:** {priority}
- **URL:** {item['url']}

## Notification Content

{item['text']}

## Suggested Actions

- [ ] Open LinkedIn and review notification
- [ ] Respond if needed
- [ ] Update CRM or contacts
- [ ] Archive after processing

## Business Context

*Add any business context or follow-up actions.*

---
*Automatically imported by LinkedIn Watcher*
'''
        
        filepath.write_text(content)
        self.logger.info(f"Created action file: {filename}")
        return filepath
    
    def run(self):
        """Main run loop with initial authentication."""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Session path: {self.session_path}')
        self.logger.info('First run: Login to LinkedIn manually')
        
        # First run - authenticate
        self._initial_auth()
        
        # Start normal monitoring
        super().run()
    
    def _initial_auth(self):
        """Perform initial authentication."""
        self.logger.info('Opening browser for LinkedIn login...')
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,
                    args=['--disable-gpu', '--no-sandbox'],
                    timeout=120000  # 2 minutes timeout
                )
                
                page = browser.pages[0] if browser.pages else browser.new_page()
                page.goto(self.LINKEDIN_URL, wait_until='domcontentloaded')
                
                self.logger.info('Please log in to LinkedIn')
                self.logger.info('Browser will stay open for 3 minutes...')
                self.logger.info('After login, close the browser manually')
                
                # Wait longer for login (3 minutes)
                for i in range(36):  # 180 seconds total
                    time.sleep(5)
                    
                    try:
                        if page.query_selector('[aria-label="Notifications"]'):
                            self.logger.info('✅ Authentication successful!')
                            self.logger.info('Session saved. You can close the browser.')
                            # Don't break - let user close browser manually
                    except:
                        pass
                
                try:
                    browser.close()
                except:
                    pass
                
                self.logger.info('Authentication complete')
                
        except Exception as e:
            self.logger.error(f'Authentication error: {e}')


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python linkedin_watcher.py <vault_path> [check_interval_seconds]")
        print("\n⚠️ WARNING: Be aware of LinkedIn's Terms of Service.")
        sys.exit(1)
    
    vault_path = sys.argv[1]
    check_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    
    if not Path(vault_path).exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    try:
        watcher = LinkedInWatcher(vault_path, check_interval=check_interval)
        watcher.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
