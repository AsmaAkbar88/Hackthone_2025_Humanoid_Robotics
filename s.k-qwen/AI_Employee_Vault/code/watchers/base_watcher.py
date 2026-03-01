#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base Watcher - Abstract base class for all AI Employee watchers.

All watchers (Gmail, WhatsApp, File System, etc.) inherit from this class
and implement the check_for_updates() and create_action_file() methods.

Usage:
    class MyWatcher(BaseWatcher):
        def check_for_updates(self) -> list:
            # Return list of new items to process
            pass
        
        def create_action_file(self, item) -> Path:
            # Create .md file in Needs_Action folder
            pass
        
        def run(self):
            # Inherited from BaseWatcher
            pass
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional


class BaseWatcher(ABC):
    """
    Abstract base class for all watcher implementations.
    
    Attributes:
        vault_path: Path to the Obsidian vault root
        needs_action: Path to the /Needs_Action folder
        check_interval: Seconds between checks (default: 60)
        logger: Logger instance for this watcher
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the base watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root directory
            check_interval: How often to check for updates (in seconds)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Ensure the Needs_Action folder exists
        self.needs_action.mkdir(parents=True, exist_ok=True)
        
        # Track processed items to avoid duplicates
        self.processed_ids: set = set()
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging to file and console."""
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory
        logs_dir = self.vault_path / 'Logs'
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        # File handler - daily rotating log
        log_file = logs_dir / f'watcher_{self.__class__.__name__}_{datetime.now().strftime("%Y-%m-%d")}.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    @abstractmethod
    def check_for_updates(self) -> list:
        """
        Check for new items that need processing.
        
        Returns:
            list: List of new items to process. Each item should be a dict
                  containing all necessary information for processing.
        
        Example:
            return [{
                'id': 'msg_123',
                'type': 'email',
                'from': 'client@example.com',
                'subject': 'Inquiry',
                'content': '...',
                'timestamp': '2026-02-27T10:30:00Z'
            }]
        """
        pass
    
    @abstractmethod
    def create_action_file(self, item: Any) -> Path:
        """
        Create a markdown action file in the Needs_Action folder.
        
        Args:
            item: Item data from check_for_updates()
        
        Returns:
            Path: Path to the created action file
        
        Example:
            Returns: Path('/vault/Needs_Action/EMAIL_msg_123.md')
        """
        pass
    
    def run(self):
        """
        Main run loop for the watcher.
        
        Continuously checks for updates and creates action files.
        Runs until interrupted (Ctrl+C).
        """
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval}s')
        
        try:
            while True:
                try:
                    items = self.check_for_updates()
                    self.logger.debug(f'Found {len(items)} new items')
                    
                    for item in items:
                        try:
                            filepath = self.create_action_file(item)
                            self.logger.info(f'Created action file: {filepath.name}')
                        except Exception as e:
                            self.logger.error(f'Error creating action file: {e}')
                    
                except Exception as e:
                    self.logger.error(f'Error in check loop: {e}')
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info(f'{self.__class__.__name__} stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}')
            raise
    
    def generate_frontmatter(self, item_type: str, **kwargs) -> str:
        """
        Generate YAML frontmatter for action files.
        
        Args:
            item_type: Type of item (email, whatsapp, file_drop, etc.)
            **kwargs: Additional frontmatter fields
        
        Returns:
            str: YAML frontmatter string including the closing ---
        """
        frontmatter = [
            '---',
            f'type: {item_type}',
            f'created: {datetime.now().isoformat()}',
            'status: pending',
        ]
        
        for key, value in kwargs.items():
            frontmatter.append(f'{key}: {value}')
        
        frontmatter.append('---')
        return '\n'.join(frontmatter)
    
    def sanitize_filename(self, name: str, max_length: int = 50) -> str:
        """
        Sanitize a string for use in filenames.
        
        Args:
            name: Original name
            max_length: Maximum length of filename
        
        Returns:
            str: Sanitized filename
        """
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        
        # Truncate if too long
        if len(name) > max_length:
            name = name[:max_length]
        
        return name.strip()


if __name__ == '__main__':
    # Example usage / testing
    print("BaseWatcher is an abstract class. Inherit from it to create watchers.")
    print("\nExample:")
    print("""
class GmailWatcher(BaseWatcher):
    def check_for_updates(self) -> list:
        # Implement Gmail checking logic
        return []
    
    def create_action_file(self, item) -> Path:
        # Implement action file creation
        return self.needs_action / 'test.md'
""")
