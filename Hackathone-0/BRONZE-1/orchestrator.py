#!/usr/bin/env python3
"""
Orchestrator for the AI Employee system.

This script coordinates the various components of the AI Employee:
- Starts watchers
- Processes tasks in the vault
- Maintains system status
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path
import threading
from vault_interaction_demo import process_needs_action_folder

# Set up logging - only show warnings and errors
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIEmployeeOrchestrator:
    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path)
        self.running = False
        self.watchers = []

        # Ensure required directories exist
        self._setup_directories()

    def _setup_directories(self):
        """Create required directories if they don't exist."""
        dirs = ['Inbox', 'Needs_Action', 'Done']
        for dir_name in dirs:
            dir_path = self.vault_path / dir_name
            dir_path.mkdir(exist_ok=True)

    def add_filesystem_watcher(self, inbox_folder: str = None):
        """Add the file system watcher."""
        from filesystem_watcher import FileSystemWatcher
        if inbox_folder is None:
            inbox_folder = str(self.vault_path / "Inbox")
        watcher = FileSystemWatcher(str(self.vault_path), inbox_folder)
        self.watchers.append(("FileSystemWatcher", watcher))

    def start_watchers(self):
        """Start all registered watchers."""
        for name, watcher in self.watchers:
            # For the file system watcher, we'll start it in a separate thread
            thread = threading.Thread(target=watcher.run, daemon=True)
            thread.start()

    def process_vault_tasks(self):
        """Process tasks in the vault."""
        try:
            process_needs_action_folder(self.vault_path)
        except Exception as e:
            logger.error(f"Error processing vault tasks: {e}")

    def periodic_vault_check(self, interval: int = 30):
        """Run periodic checks on the vault."""
        while self.running:
            self.process_vault_tasks()
            time.sleep(interval)

    def start(self):
        """Start the orchestrator."""

        # Add the file system watcher
        self.add_filesystem_watcher()

        # Start watchers
        self.start_watchers()

        # Start periodic vault checking in a separate thread
        vault_thread = threading.Thread(
            target=self.periodic_vault_check,
            args=(30,),  # Check every 30 seconds
            daemon=True
        )
        vault_thread.start()

        self.running = True

        try:
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the orchestrator."""
        self.running = False

def main():
    # Check if required dependencies are installed
    try:
        import watchdog
    except ImportError:
        print("Watchdog library not found. Please install with: pip install -r requirements.txt")
        return 1

    # Create and start the orchestrator
    orchestrator = AIEmployeeOrchestrator()

    print("AI Employee Orchestrator")
    print("================================================")
    print("Starting the Bronze Tier implementation...")
    print("Features:")
    print("- File System Watcher monitoring Inbox folder")
    print("- Vault interaction (reading/writing to Obsidian vault)")
    print("- Basic folder structure (Inbox, Needs_Action, Done)")
    print("- Dashboard.md and Company_Handbook.md available")
    print("")
    print("================================================")
    print("Use Ctrl+C to stop the orchestrator")
    print("Place files in the Inbox folder to trigger processing")
    print("")

    orchestrator.start()

    return 0

if __name__ == "__main__":
    sys.exit(main())