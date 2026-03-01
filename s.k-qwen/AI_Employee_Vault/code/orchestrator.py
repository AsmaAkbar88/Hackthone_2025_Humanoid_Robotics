#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrator - Master process for AI Employee.

The Orchestrator:
1. Monitors the Needs_Action folder for new tasks
2. Triggers Claude Code to process tasks
3. Manages the approval workflow
4. Updates the Dashboard
5. Handles task completion and archiving

Usage:
    python orchestrator.py <vault_path> [--claude-command <command>]

Example:
    python orchestrator.py /path/to/AI_Employee_Vault
    python orchestrator.py /path/to/AI_Employee_Vault --claude-command "claude"

Features:
    - Polls Needs_Action folder for new tasks
    - Generates prompts for Claude Code
    - Moves completed tasks to /Done
    - Updates Dashboard.md with status
    - Logs all operations
"""

import sys
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import argparse


class Orchestrator:
    """
    Main orchestrator for the AI Employee system.
    
    Coordinates between watchers, Claude Code, and the file system
    to process tasks autonomously.
    """
    
    def __init__(self, vault_path: str, claude_command: str = "claude"):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault
            claude_command: Command to invoke Claude Code (default: "claude")
        """
        self.vault_path = Path(vault_path)
        self.claude_command = claude_command
        
        # Folder paths
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.approved = self.vault_path / 'Approved'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.rejected = self.vault_path / 'Rejected'
        self.logs = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'
        
        # Ensure all folders exist
        for folder in [self.needs_action, self.done, self.plans, 
                       self.approved, self.pending_approval, self.rejected, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Track processed files
        self.processed_files: set = set()
        
        # Statistics
        self.stats = {
            'tasks_processed': 0,
            'tasks_completed': 0,
            'approvals_pending': 0,
            'errors': 0
        }
    
    def _setup_logging(self):
        """Setup logging configuration."""
        import logging
        
        log_file = self.logs / f'orchestrator_{datetime.now().strftime("%Y-%m-%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger('Orchestrator')
    
    def get_pending_tasks(self) -> List[Path]:
        """
        Get list of pending task files in Needs_Action.
        
        Returns:
            List[Path]: List of .md files waiting to be processed
        """
        if not self.needs_action.exists():
            return []
        
        pending = []
        for f in self.needs_action.glob('*.md'):
            if f not in self.processed_files:
                pending.append(f)
        
        return sorted(pending, key=lambda x: x.stat().st_mtime)
    
    def get_approved_actions(self) -> List[Path]:
        """
        Get list of approved actions ready for execution.
        
        Returns:
            List[Path]: Files in /Approved folder
        """
        if not self.approved.exists():
            return []
        
        return list(self.approved.glob('*.md'))
    
    def read_file(self, filepath: Path) -> str:
        """Read file content."""
        try:
            return filepath.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            # Try with default encoding
            return filepath.read_text()
        except Exception as e:
            self.logger.error(f'Error reading {filepath}: {e}')
            return ""
    
    def create_plan(self, task_file: Path, plan_content: str) -> Path:
        """
        Create a plan file for a task.
        
        Args:
            task_file: Original task file
            plan_content: Content for the plan
        
        Returns:
            Path: Path to created plan file
        """
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        plan_name = f'PLAN_{task_file.stem}_{timestamp}.md'
        plan_path = self.plans / plan_name
        
        plan_path.write_text(plan_content)
        self.logger.info(f'Created plan: {plan_path.name}')
        
        return plan_path
    
    def update_dashboard(self, update_type: str, **kwargs):
        """
        Update the Dashboard.md with new information.
        
        Args:
            update_type: Type of update (task_completed, approval_needed, etc.)
            **kwargs: Additional data for the update
        """
        if not self.dashboard.exists():
            self.logger.warning('Dashboard.md not found')
            return
        
        content = self.dashboard.read_text()
        
        # Update timestamp
        content = content.replace(
            'last_updated:', 
            f'last_updated: {datetime.now().isoformat()}'
        )
        
        # Update pending actions count
        pending_count = len(self.get_pending_tasks())
        # This is a simple update - in production you'd parse and update the table
        
        self.dashboard.write_text(content)
        self.logger.debug(f'Dashboard updated: {update_type}')
    
    def process_task(self, task_file: Path) -> bool:
        """
        Process a single task file using Claude Code.

        Args:
            task_file: Path to the task file in Needs_Action

        Returns:
            bool: True if processing succeeded
        """
        self.logger.info(f'Processing task: {task_file.name}')

        try:
            # Read the task file
            task_content = self.read_file(task_file)

            if not task_content.strip():
                self.logger.warning(f'Empty task file: {task_file.name}')
                return False

            # Create prompt for Claude
            prompt = self._create_claude_prompt(task_file, task_content)

            # Run Claude Code
            result = self._run_claude(prompt)

            if result:
                # Mark as processed
                self.processed_files.add(task_file)
                self.stats['tasks_processed'] += 1

                # Move task file to Done
                self._move_to_done(task_file)

                # Update dashboard
                self.update_dashboard('task_processed', task=task_file.name)

                return True
            else:
                self.stats['errors'] += 1
                return False

        except Exception as e:
            self.logger.error(f'Error processing task: {e}')
            self.stats['errors'] += 1
            return False

    def _move_to_done(self, task_file: Path):
        """Move task file and its metadata to Done folder."""
        try:
            # Move the .md file
            if task_file.exists():
                dest = self.done / task_file.name
                shutil.move(str(task_file), str(dest))
                self.logger.info(f'Moved to Done: {task_file.name}')

            # Move associated .txt file if exists
            txt_file = task_file.with_suffix('.txt')
            if txt_file.exists():
                dest = self.done / txt_file.name
                shutil.move(str(txt_file), str(dest))
                self.logger.info(f'Moved to Done: {txt_file.name}')
        except Exception as e:
            self.logger.error(f'Error moving to Done: {e}')
    
    def _create_claude_prompt(self, task_file: Path, task_content: str) -> str:
        """
        Create a prompt for Claude Code to process the task.
        
        Args:
            task_file: Path to the task file
            task_content: Content of the task file
        
        Returns:
            str: Prompt for Claude
        """
        # Read Company Handbook for context
        handbook_path = self.vault_path / 'Company_Handbook.md'
        handbook_content = self.read_file(handbook_path) if handbook_path.exists() else ""
        
        # Read Business Goals
        goals_path = self.vault_path / 'Business_Goals.md'
        goals_content = self.read_file(goals_path) if goals_path.exists() else ""
        
        prompt = f"""You are an AI Employee assistant. Process the following task according to the Company Handbook.

## Context

### Company Handbook Rules
{handbook_content[:5000] if handbook_content else "No handbook found."}

### Business Goals
{goals_content[:2000] if goals_content else "No goals found."}

## Task File: {task_file.name}

{task_content}

## Instructions

1. **Analyze** the task and identify what needs to be done
2. **Check** if this requires human approval (see Company Handbook)
3. **Create** a Plan.md file in /Plans with:
   - Clear objective
   - Step-by-step checklist
   - Approval requirements (if any)
4. **Take action** if no approval needed, or create approval request in /Pending_Approval
5. **Move** this task file to /Done when complete (or when waiting for approval)

## Output Format

After processing, output:
- Summary of actions taken
- Any files created
- Next steps required

Remember: Always follow the Rules of Engagement in the Company Handbook.
When in doubt, request human approval.
"""
        
        return prompt
    
    def _run_claude(self, prompt: str) -> bool:
        """
        Run Claude Code with the given prompt.

        Args:
            prompt: Prompt to send to Claude

        Returns:
            bool: True if Claude executed successfully
        """
        try:
            # Change to vault directory
            original_dir = Path.cwd()

            # Run Claude Code (use shell=True on Windows to find npm-installed commands)
            # Note: Claude Code 2.1+ uses -p/--print instead of --prompt
            import platform
            use_shell = platform.system() == 'Windows'
            
            process = subprocess.Popen(
                [self.claude_command, '-p', prompt],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(self.vault_path),
                shell=use_shell
            )
            
            stdout, stderr = process.communicate(timeout=300)  # 5 minute timeout

            # Log output (handle encoding issues)
            if stdout:
                try:
                    self.logger.info(f'Claude output: {stdout[:500]}')
                except UnicodeEncodeError:
                    self.logger.info(f'Claude output: {stdout[:200].encode("ascii", errors="ignore")}')
            
            if stderr:
                self.logger.warning(f'Claude stderr: {stderr[:500]}')

            return process.returncode == 0
            
        except subprocess.TimeoutExpired:
            self.logger.error('Claude Code timed out')
            return False
        except FileNotFoundError:
            self.logger.error(f'Claude Code not found: {self.claude_command}')
            self.logger.error('Make sure Claude Code is installed: npm install -g @anthropic/claude-code')
            return False
        except Exception as e:
            self.logger.error(f'Error running Claude: {e}')
            return False
    
    def process_approved_actions(self) -> bool:
        """
        Process actions that have been approved by human.
        
        Returns:
            bool: True if any actions were processed
        """
        approved_files = self.get_approved_actions()
        
        if not approved_files:
            return False
        
        for approved_file in approved_files:
            self.logger.info(f'Processing approved action: {approved_file.name}')
            
            # Read the approved action
            content = self.read_file(approved_file)
            
            # Execute the action (this would integrate with MCP servers in Silver/Gold tier)
            # For Bronze tier, we just log and move to Done
            
            # Move to Done
            dest = self.done / approved_file.name
            shutil.move(str(approved_file), str(dest))
            
            self.logger.info(f'Approved action completed: {dest.name}')
            self.stats['tasks_completed'] += 1
        
        return True
    
    def log_operation(self, operation: str, details: Dict[str, Any]):
        """
        Log an operation to the daily log file.
        
        Args:
            operation: Operation type
            details: Operation details
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'details': details
        }
        
        log_file = self.logs / f'{datetime.now().strftime("%Y-%m-%d")}.json'
        
        # Read existing logs
        logs = []
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text())
            except:
                logs = []
        
        logs.append(log_entry)
        
        # Write back
        log_file.write_text(json.dumps(logs, indent=2))
    
    def run(self, poll_interval: int = 30):
        """
        Main run loop.
        
        Args:
            poll_interval: Seconds between checks (default: 30)
        """
        self.logger.info('=' * 50)
        self.logger.info('AI Employee Orchestrator Starting')
        self.logger.info(f'Vault: {self.vault_path}')
        self.logger.info(f'Poll interval: {poll_interval}s')
        self.logger.info('=' * 50)
        
        try:
            while True:
                # Check for pending tasks
                pending_tasks = self.get_pending_tasks()
                
                if pending_tasks:
                    self.logger.info(f'Found {len(pending_tasks)} pending task(s)')
                    
                    for task in pending_tasks:
                        self.process_task(task)
                
                # Check for approved actions
                if self.get_approved_actions():
                    self.process_approved_actions()
                
                # Update stats
                self.stats['approvals_pending'] = len(self.get_approved_actions())
                
                # Log periodic stats
                if self.stats['tasks_processed'] % 10 == 0:
                    self.logger.info(f'Stats: {self.stats}')
                
                # Wait before next poll
                import time
                time.sleep(poll_interval)
                
        except KeyboardInterrupt:
            self.logger.info('Orchestrator stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}')
            raise
        
        # Final stats
        self.logger.info(f'Final Stats: {self.stats}')


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='AI Employee Orchestrator - Process tasks from Needs_Action folder'
    )
    parser.add_argument(
        'vault_path',
        help='Path to the Obsidian vault'
    )
    parser.add_argument(
        '--claude-command',
        default='claude',
        help='Command to invoke Claude Code (default: claude)'
    )
    parser.add_argument(
        '--poll-interval',
        type=int,
        default=30,
        help='Seconds between checks (default: 30)'
    )
    
    args = parser.parse_args()
    
    vault = Path(args.vault_path)
    if not vault.exists():
        print(f"Error: Vault path does not exist: {args.vault_path}")
        sys.exit(1)
    
    orchestrator = Orchestrator(str(vault), args.claude_command)
    orchestrator.run(args.poll_interval)


if __name__ == '__main__':
    main()
