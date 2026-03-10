#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail Watcher - Monitors Gmail for new important messages.

When new unread important emails arrive, this watcher creates
action files in the Needs_Action folder for AI processing.

Usage:
    python gmail_watcher.py <vault_path> [check_interval_seconds]

Example:
    python gmail_watcher.py ../ 120

Prerequisites:
    1. Enable Gmail API: https://developers.google.com/gmail/api/quickstart/python
    2. Download credentials.json and place in same directory
    3. First run will open browser for OAuth authorization
    4. token.json will be created automatically

Features:
    - Monitors Gmail for unread important messages
    - Filters by keywords (urgent, invoice, payment, etc.)
    - Creates markdown action files with email metadata
    - Tracks processed message IDs to avoid duplicates
"""

import sys
import os
import base64
from pathlib import Path
from datetime import datetime
from email import message_from_bytes

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from base_watcher import BaseWatcher

# Gmail API dependencies
try:
    from google.oauth2.credentials import Credentials
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False
    print("Gmail dependencies not installed. Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")


class GmailWatcher(BaseWatcher):
    """
    Gmail Watcher that monitors for new important emails.
    
    Attributes:
        creds_path: Path to credentials.json
        token_path: Path to token.json (auto-generated)
        keywords: List of keywords to filter important emails
        check_interval: Seconds between checks (default: 120)
    """
    
    # If modifying scopes, delete token.json
    # Using specific scopes for reading AND sending emails
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.compose'
    ]
    
    # Keywords that indicate important emails
    # Now includes common words to catch most emails
    KEYWORDS = ['urgent', 'asap', 'invoice', 'payment', 'important',
                'action required', 'deadline', 'reminder', 'hello', 'hi',
                'test', 'email', 'message', 'reply', 'thanks', 'thank you',
                'meeting', 'call', 'update', 'info', 'question', 'help']
    
    # Process ALL unread emails (not just keyword-matched)
    PROCESS_ALL_UNREAD = True
    
    def __init__(self, vault_path: str, credentials_path: str = None, 
                 check_interval: int = 120):
        """
        Initialize the Gmail watcher.

        Args:
            vault_path: Path to the Obsidian vault
            credentials_path: Path to Gmail credentials.json
            check_interval: How often to check for new emails (seconds)
        """
        super().__init__(vault_path, check_interval)

        if not GMAIL_AVAILABLE:
            raise ImportError("Gmail dependencies not installed")

        # Set credentials path
        self.credentials_path = Path(credentials_path) if credentials_path else Path(__file__).parent / 'credentials.json'
        self.token_path = Path(__file__).parent / 'token.json'
        self.cache_file = Path(__file__).parent / 'gmail_cache.json'

        # CLEAR CACHE on init - process ALL unread emails every time!
        if self.cache_file.exists():
            self.cache_file.unlink()
            self.logger.info('[OK] Cache cleared - will process ALL unread emails')

        # Initialize Gmail service
        self.service = self._authenticate()

        # Track processed message IDs (only for this session)
        self.processed_ids = set()
    
    def _authenticate(self):
        """
        Authenticate with Gmail API.
        
        Returns:
            Gmail API service object
        """
        creds = None
        
        # Load token.json if exists
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(
                self.token_path, self.SCOPES
            )
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self.credentials_path.exists():
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_path}\n"
                        "Download from: https://developers.google.com/gmail/api/quickstart/python"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            self.token_path.write_text(creds.to_json())
        
        return build('gmail', 'v1', credentials=creds)
    
    def _is_important(self, headers: dict, snippet: str) -> bool:
        """
        Check if email is important based on keywords.
        If PROCESS_ALL_UNREAD is True, all emails are considered important.

        Args:
            headers: Email headers dict
            snippet: Email body snippet

        Returns:
            bool: True if email is important
        """
        # If PROCESS_ALL_UNREAD is True, process all emails
        if self.PROCESS_ALL_UNREAD:
            return True
        
        text = f"{headers.get('Subject', '')} {snippet}".lower()
        return any(keyword in text for keyword in self.KEYWORDS)
    
    def check_for_updates(self) -> list:
        """
        Check Gmail for new important messages.
        Fetches FULL email body for better reply generation.
        Processes ALL unread emails every time.

        Returns:
            list: List of new message dicts with id, snippet, headers, body
        """
        try:
            # Search for ALL unread messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=50
            ).execute()

            messages = results.get('messages', [])
            new_messages = []
            
            # Track processed in THIS run (prevent duplicates)
            this_run_ids = set()

            for msg in messages:
                msg_id = msg['id']

                # Skip if already processed in THIS session
                if msg_id in self.processed_ids:
                    self.logger.debug(f'Skipping already processed: {msg_id}')
                    continue
                
                # Skip if already processed in THIS run (prevent duplicates)
                if msg_id in this_run_ids:
                    self.logger.debug(f'Skipping duplicate in this run: {msg_id}')
                    continue

                # Get FULL message details with body
                message = self.service.users().messages().get(
                    userId='me',
                    id=msg_id,
                    format='full'  # Get full message with body parts
                ).execute()

                # Extract headers
                headers = message['payload']['headers']
                header_dict = {h['name']: h['value'] for h in headers}

                # Extract FULL email body
                email_body = self._extract_email_body(message['payload'])

                # Get snippet (fallback)
                snippet = message['snippet']
                if not snippet and email_body:
                    snippet = email_body[:200]

                # Check if important
                is_important = self._is_important(header_dict, snippet)

                if is_important:
                    new_messages.append({
                        'id': msg_id,
                        'type': 'email',
                        'from': header_dict.get('From', 'Unknown'),
                        'to': header_dict.get('To', ''),
                        'subject': header_dict.get('Subject', 'No Subject'),
                        'date': header_dict.get('Date', ''),
                        'snippet': snippet[:500],
                        'body': email_body,
                        'labels': message.get('labelIds', [])
                    })

                    # Mark as processed for THIS session
                    self.processed_ids.add(msg_id)
                    # Mark as processed in THIS run
                    this_run_ids.add(msg_id)

                    self.logger.info(f'Processing email: {msg_id}')
                    if email_body:
                        self.logger.debug(f'Email body: {email_body[:100]}...')

            self.logger.info(f'Found {len(new_messages)} new email(s)')
            return new_messages

        except HttpError as error:
            self.logger.error(f"Gmail API error: {error}")
            return []
        except Exception as error:
            self.logger.error(f"Error checking Gmail: {error}")
            return []

    def _extract_email_body(self, payload) -> str:
        """
        Extract the full email body from the message payload.
        Handles multipart messages and attachments.
        """
        body = ""
        
        try:
            # Check if multipart
            if payload.get('mimeType', '').startswith('multipart/'):
                # Get parts (prefer text/plain over text/html)
                parts = payload.get('parts', [])
                
                # First try to find text/plain part
                for part in parts:
                    if part.get('mimeType') == 'text/plain':
                        body_data = part.get('body', {}).get('data', '')
                        if body_data:
                            body = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
                            break
                
                # If no text/plain, try text/html
                if not body:
                    for part in parts:
                        if part.get('mimeType') == 'text/html':
                            body_data = part.get('body', {}).get('data', '')
                            if body_data:
                                body = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
                                # Simple HTML cleanup
                                body = body.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
                                body = body.replace('<p>', '\n').replace('</p>', '\n')
                                # Remove remaining HTML tags
                                import re
                                body = re.sub(r'<[^>]+>', '', body)
                                break
                
                # If still no body, try recursive search in nested parts
                if not body:
                    for part in parts:
                        nested_body = self._extract_email_body(part)
                        if nested_body:
                            body = nested_body
                            break
            
            # Single part message
            elif payload.get('body', {}).get('data', ''):
                body_data = payload['body']['data']
                body = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
        
        except Exception as e:
            self.logger.warning(f'Error extracting email body: {e}')
        
        return body.strip() if body else ""
    
    def _is_important(self, headers: dict, snippet: str) -> bool:
        """
        Check if email is important based on keywords.
        If PROCESS_ALL_UNREAD is True, all emails are considered important.

        Args:
            headers: Email headers dict
            snippet: Email body snippet

        Returns:
            bool: True if email is important
        """
        # If PROCESS_ALL_UNREAD is True, process all emails
        if self.PROCESS_ALL_UNREAD:
            return True
        
        text = f"{headers.get('Subject', '')} {snippet}".lower()
        return any(keyword in text for keyword in self.KEYWORDS)
    
    def create_action_file(self, item: dict) -> Path:
        """
        Create a markdown action file for the email.
        Checks for duplicates before creating.
        """
        # Generate filename
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        subject_safe = self.sanitize_filename(item['subject'], 30)
        filename = f"EMAIL_{timestamp}_{subject_safe}.md"
        filepath = self.needs_action / filename

        # CHECK FOR DUPLICATES - Same gmail_id already exists
        for existing_file in self.needs_action.glob('*.md'):
            existing_content = existing_file.read_text(encoding='utf-8')
            if f"gmail_id: {item['id']}" in existing_content:
                self.logger.warning(f'Duplicate email {item["id"]} - file already exists: {existing_file.name}')
                return existing_file  # Return existing file, don't create duplicate

        # Check if file already exists (prevent duplicates)
        if filepath.exists():
            self.logger.warning(f'File already exists, skipping: {filename}')
            return filepath
        
        # Parse date
        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(item['date'])
            date_str = dt.isoformat()
        except:
            date_str = datetime.now().isoformat()
        
        # Determine priority
        priority = 'high' if any(kw in item['subject'].lower() for kw in ['urgent', 'asap']) else 'normal'

        # Get full email body
        email_body = item.get('body', '')
        if not email_body:
            email_body = item.get('snippet', 'No content available')

        # Create content with FULL email body
        content = f'''---
type: email
from: {item['from']}
to: {item['to']}
subject: {item['subject']}
received: {date_str}
priority: {priority}
status: pending
gmail_id: {item['id']}
---

# Email Received

## Header Information

- **From:** {item['from']}
- **To:** {item['to']}
- **Subject:** {item['subject']}
- **Received:** {date_str}
- **Priority:** {priority}

## Email Content

{email_body}

## Suggested Actions

- [ ] Read full email in Gmail
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing

## Notes

*Add any notes or context for processing this email.*

---
*Automatically imported by Gmail Watcher*
'''
        
        filepath.write_text(content, encoding='utf-8')
        self.logger.info(f"Created action file: {filename}")
        # Console pe clean output
        print(f"✅ New email from {item['from'].split('<')[0].strip()}: {item['subject']}")
        
        return filepath


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python gmail_watcher.py <vault_path> [check_interval_seconds]")
        print("\nExample:")
        print("  python gmail_watcher.py ../ 120")
        print("\nSetup:")
        print("  1. Download credentials.json from Google Cloud Console")
        print("  2. Place in same directory as gmail_watcher.py")
        print("  3. First run will open browser for OAuth authorization")
        sys.exit(1)
    
    vault_path = sys.argv[1]
    check_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    
    if not Path(vault_path).exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    try:
        watcher = GmailWatcher(vault_path, check_interval=check_interval)
        watcher.run()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
