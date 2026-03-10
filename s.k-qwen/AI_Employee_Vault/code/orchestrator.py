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
import time
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
        Process a single task file.

        Clean terminal flow:
        1. Show minimal header
        2. Show email summary (clean)
        3. Get user reply
        4. Show progress
        5. Show clean success message

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

            # Extract email details
            email_from = ""
            email_subject = ""
            email_body = ""
            in_body = False

            for line in task_content.split('\n'):
                line_lower = line.lower().strip()
                
                # Extract FROM (skip type: email line)
                if 'from:' in line_lower and not email_from and 'type:' not in line_lower:
                    email_from = line.split(':', 1)[1].strip()
                # Extract SUBJECT
                elif 'subject:' in line_lower and not email_subject:
                    email_subject = line.split(':', 1)[1].strip()
                # Start of email content section
                elif '## email content' in line_lower:
                    in_body = True
                # End of email content (new section or separator)
                elif in_body and (line.startswith('##') or line.startswith('---')):
                    break
                # Collect email body lines
                elif in_body:
                    # Skip checkboxes, empty lines, and metadata
                    stripped = line.strip()
                    if stripped and not stripped.startswith('- [ ]') and not stripped.startswith('- [x]'):
                        if 'automatically imported' not in line.lower() and 'add any notes' not in line.lower():
                            email_body += line + '\n'

            # Clean terminal output
            print("\n" + "=" * 60)
            print(f"📧 New Email: {email_subject}")
            print(f"   From: {email_from}")
            print("-" * 60)
            
            # Show email body (clean, max 3 lines)
            body_lines = [l.strip() for l in email_body.split('\n') 
                         if l.strip() and not l.startswith('##') and not l.startswith('[')]
            for i, line in enumerate(body_lines[:3]):
                print(f"   {line}")
            if len(body_lines) > 3:
                print("   ...")
            
            print("-" * 60)

            # Get user's reply
            try:
                user_reply = input("\n💬 Your reply (Roman Urdu/English): ").strip()
            except KeyboardInterrupt:
                print("\n❌ Cancelled\n")
                return False

            if not user_reply:
                print("\n❌ No reply provided\n")
                return False

            self.logger.info(f'User reply: {user_reply}')

            # Convert to English
            print("\n⏳ Converting to English...", end="", flush=True)
            simple_reply = self._convert_to_simple_english(email_subject, email_from, user_reply)
            print(" ✓")

            # Create Plan
            print("📝 Creating plan...", end="", flush=True)
            plan = self._create_plan_for_task(task_file, task_content)
            print(" ✓")

            # Create Approval
            print("📋 Creating approval request...", end="", flush=True)
            self._create_approval_request_with_reply(task_file, task_content, plan, simple_reply)
            print(" ✓")

            # Move to Pending_Approval
            self._move_to_pending_approval(task_file)

            # Clean success message
            print("\n" + "=" * 60)
            print("✅ SUCCESS!")
            print("-" * 60)
            print(f"   Reply: \"{simple_reply.replace(chr(10), ' ')}\"")
            print("-" * 60)
            print("📂 Next: Move APPROVAL file to /Approved/ to send")
            print("=" * 60 + "\n")

            return True

        except Exception as e:
            self.logger.error(f'Error processing task: {e}')
            self.stats['errors'] += 1
            print(f"\n❌ Error: {e}\n")
            return False

    def _create_plan_for_task(self, task_file: Path, task_content: str) -> dict:
        """
        Create a Plan.md file for the task.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        plan_name = f'PLAN_{task_file.stem}_{timestamp}.md'
        plan_path = self.plans / plan_name
        
        # Extract objective from task
        objective = self._extract_objective(task_content)
        
        # Generate steps based on task type
        steps = self._generate_steps(task_content)
        
        # Build checklist
        checklist = '\n'.join([f'- [ ] {step}' for step in steps])
        
        content = f'''---
type: plan
source_task: {task_file.name}
created: {datetime.now().isoformat()}
status: in_progress
objective: {objective}
---

# Plan: {objective}

## Source Task
{task_file.name}

## Objective

{objective}

## Steps

{checklist}

## Approval Required
Yes - Human approval needed before execution

## Status
Waiting for approval...

---
*Generated by AI Employee Orchestrator*
'''
        
        plan_path.write_text(content, encoding='utf-8')
        self.logger.info(f'[OK] Plan created: {plan_name}')
        
        return {
            'name': plan_name,
            'path': plan_path,
            'objective': objective,
            'steps': steps
        }

    def _extract_objective(self, content: str) -> str:
        """Extract objective from task content."""
        # Look for # or ## header
        import re
        match = re.search(r'#\s*(.+?)(?:\n|$)', content)
        if match:
            return match.group(1).strip()
        
        # Fallback
        return 'Complete task'

    def _generate_steps(self, task_content: str) -> List[str]:
        """Generate steps based on task type."""
        content_lower = task_content.lower()
        
        # LinkedIn post steps
        if 'linkedin' in content_lower:
            return [
                'Review post content',
                'Check for spelling and grammar',
                'Verify hashtags are relevant',
                'Create approval request',
                'Wait for human approval',
                'Post to LinkedIn',
                'Verify post was published',
                'Log the action',
                'Move to Done'
            ]
        
        # Email steps
        elif 'email' in content_lower:
            return [
                'Review email content',
                'Verify recipient address',
                'Check attachments',
                'Create approval request',
                'Wait for human approval',
                'Send email via MCP',
                'Verify email sent',
                'Log the action',
                'Move to Done'
            ]
        
        # Generic steps
        return [
            'Analyze task requirements',
            'Identify required actions',
            'Check for approval requirements',
            'Execute action',
            'Verify completion',
            'Log the action',
            'Move to Done'
        ]

    def _move_to_pending_approval(self, task_file: Path):
        """Move task file to Pending_Approval folder."""
        try:
            dest = self.pending_approval / task_file.name
            shutil.move(str(task_file), str(dest))
            self.logger.info(f'[OK] Moved to Pending_Approval: {task_file.name}')
        except Exception as e:
            self.logger.error(f'Error moving to Pending_Approval: {e}')

    def _check_requires_approval(self, task_content: str, task_file: Path = None) -> bool:
        """
        Check if task requires human approval based on content.

        Also checks the original Inbox file if available.
        """
        content_lower = task_content.lower()
        filename = task_file.name.lower() if task_file else ''

        # First check current file content
        if 'linkedin' in filename or 'linkedin' in content_lower:
            self.logger.info('[INFO] LinkedIn post detected - approval required')
            return True
        
        # Check for EMAIL tasks - always require approval for replies
        if 'type: email' in content_lower or filename.startswith('email_'):
            self.logger.info('[INFO] Email detected - approval required for reply')
            return True

        # If this is a FILE_DROP file, check the original Inbox file
        if task_file and 'FILE_DROP' in task_file.name:
            # Extract original filename from FILE_DROP name
            # FILE_DROP_2026-03-05_08-21-53_graphic-design-first-day.md
            parts = task_file.stem.split('_')
            if len(parts) >= 5:
                original_name = '_'.join(parts[4:]) + '.md'  # Skip FILE, DROP, date, time
                inbox_file = self.vault_path / 'Inbox' / original_name

                if inbox_file.exists():
                    self.logger.info(f'[INFO] Checking original file: {original_name}')
                    inbox_content = inbox_file.read_text(encoding='utf-8').lower()
                    if 'linkedin' in inbox_content:
                        self.logger.info('[INFO] LinkedIn post detected in original file - approval required')
                        return True

        # Keywords that trigger approval requirement
        approval_keywords = [
            'send email', 'send message', 'post to',
            'payment', 'pay $', 'transfer',
            'delete', 'remove', 'cancel subscription',
            'approve', 'confirmation required'
        ]

        return any(kw in content_lower for kw in approval_keywords)

    def _create_approval_request(self, task_file: Path, task_content: str, plan: dict = None):
        """
        Create an approval request file in Pending_Approval folder.
        Generates a reply draft using Claude Code automatically.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        approval_filename = f"APPROVAL_{task_file.stem}_{timestamp}.md"
        approval_path = self.pending_approval / approval_filename

        # Generate reply draft using Claude Code
        self.logger.info('[INFO] Generating reply draft with Claude Code...')
        reply_draft = self._generate_email_reply_for_approval(task_content)

        plan_info = ""
        if plan:
            plan_info = f"\n**Plan Created:** {plan['name']}\n"

        content = f'''---
type: approval_request
source_task: {task_file.name}
created: {datetime.now().isoformat()}
expires: {(datetime.now().replace(hour=23, minute=59)).isoformat()}
status: pending
action_required: human_review
{plan_info}
---

# Approval Required

## Source Task
{task_file.name}

## Plan Summary
{plan['objective'] if plan else 'Task requires approval'}

{plan_info}

## Email Content

{task_content}

## 📝 AI-Generated Reply Draft

```
{reply_draft}
```

**Note:** You can edit this reply before sending.

## Instructions

This task requires human approval before proceeding.

### To Approve
1. Review the email and reply draft above
2. Edit the reply if needed (optional)
3. Move this file to `/Approved/` folder
4. Gmail will open in browser with reply pre-filled
5. Review and click Send in Gmail

### To Reject
1. Move this file to `/Rejected/` folder
2. The task will be cancelled

---
*Created by AI Employee Orchestrator*
'''

        # Write with UTF-8 encoding to support emojis
        approval_path.write_text(content, encoding='utf-8')
        self.logger.info(f'Created approval request: {approval_filename}')

    def _create_approval_request_with_reply(self, task_file: Path, task_content: str, plan: dict, reply_draft: str):
        """
        Create an approval request file with pre-generated reply draft.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        approval_filename = f"APPROVAL_{task_file.stem}_{timestamp}.md"
        approval_path = self.pending_approval / approval_filename

        plan_info = ""
        if plan:
            plan_info = f"\n**Plan Created:** {plan['name']}\n"

        content = f'''---
type: approval_request
source_task: {task_file.name}
created: {datetime.now().isoformat()}
expires: {(datetime.now().replace(hour=23, minute=59)).isoformat()}
status: pending
action_required: human_review
{plan_info}
---

# Approval Required

## Source Task
{task_file.name}

## Plan Summary
{plan['objective'] if plan else 'Task requires approval'}

{plan_info}

## Email Content

{task_content}

## 📝 AI-Generated Reply Draft

```
{reply_draft}
```

**Note:** You can edit this reply before sending.

## Instructions

This task requires human approval before proceeding.

### To Approve
1. Review the email and reply draft above
2. Edit the reply if needed (optional)
3. Move this file to `/Approved/` folder
4. Gmail will open in browser with reply pre-filled
5. Review and click Send in Gmail

### To Reject
1. Move this file to `/Rejected/` folder
2. The task will be cancelled

---
*Created by AI Employee Orchestrator*
'''

        # Write with UTF-8 encoding to support emojis
        approval_path.write_text(content, encoding='utf-8')
        self.logger.info(f'Created approval request: {approval_filename}')

    def _convert_to_simple_english(self, subject: str, recipient: str, user_reply: str) -> str:
        """
        Convert user's reply to SIMPLE ENGLISH using Claude Code.
        Uses temp file approach (same as _generate_email_reply_for_approval).
        """
        import subprocess
        import platform
        import tempfile

        # Extract sender name
        sender_name = "there"
        if '<' in recipient:
            name_part = recipient.split('<')[0].strip()
            if name_part:
                sender_name = name_part.split()[0].capitalize()
        elif recipient:
            sender_name = recipient.split('@')[0].capitalize() if '@' in recipient else recipient.capitalize()

        # STRICT PROMPT - Direct translation only, NO conversation
        prompt_text = f"""You are a translation machine. Do NOT converse. Do NOT ask questions. Do NOT explain.

Your ONLY job: Translate Roman Urdu to English.

Roman Urdu: "{user_reply}"

English translation (output ONLY these words, nothing else):"""

        use_shell = platform.system() == 'Windows'
        self.logger.info(f'[CLAUDE] Translating: {user_reply[:50]}...')

        # Create temp file with prompt (same approach as _generate_email_reply_for_approval)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(prompt_text)
            temp_file = f.name

        try:
            # Run: type temp_file | claude  (Windows) or claude < temp_file (Unix)
            cmd = f'type "{temp_file}" | claude' if use_shell else f'claude < "{temp_file}"'

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=use_shell
            )

            stdout, stderr = process.communicate(timeout=60)

            if stdout and process.returncode == 0 and stdout.strip():
                reply = stdout.strip()
                
                # Add greeting if missing
                if not reply.lower().startswith('dear') and not reply.lower().startswith('hi') and not reply.lower().startswith('hello'):
                    reply = f"Dear {sender_name},\n\n{reply}"

                reply = reply.strip('"').strip("'").strip()

                # Ensure it ends properly
                if not reply.endswith(('.', '!', '?')):
                    reply += '.'

                self.logger.info(f'[OK] Claude translated: {reply[:100]}...')
                return reply
            else:
                # Error
                error_msg = stderr if stderr else "Claude returned empty response"
                self.logger.error(f'[FAIL] Claude failed: {error_msg}')
                raise Exception(f"Claude Code failed to convert reply. Error: {error_msg}")
        finally:
            # Clean up temp file
            try:
                import os
                os.unlink(temp_file)
            except:
                pass

    def _generate_email_reply_for_approval(self, email_content: str) -> str:
        """
        Generate a human-like email reply using Claude Code.
        Reads the actual email content and generates contextual reply.
        Uses temporary file for reliable prompt passing.
        """
        try:
            import subprocess
            import platform
            import tempfile
            import os
            
            # Extract email details
            from_email = ""
            subject = ""
            email_body = ""
            in_body = False
            
            for line in email_content.split('\n'):
                line_lower = line.lower()
                if 'from:' in line_lower and not from_email:
                    from_email = line.split(':', 1)[1].strip()
                if 'subject:' in line_lower and not subject:
                    subject = line.split(':', 1)[1].strip()
                if '## email content' in line_lower:
                    in_body = True
                    continue
                if in_body:
                    if line.startswith('##') or line.startswith('---'):
                        break
                    email_body += line + '\n'
            
            # Build prompt for Claude
            prompt_text = f"""Read this email and write a natural reply:

SUBJECT: {subject}
FROM: {from_email}
MESSAGE: {email_body[:300] if email_body else 'No message'}

Write a casual, human reply (1-3 sentences). No signatures. Just the reply text.

REPLY: """
            
            # Use temporary file for prompt (Windows compatible)
            use_shell = platform.system() == 'Windows'
            
            # Create temp file with prompt
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(prompt_text)
                temp_file = f.name
            
            try:
                # Run: claude < temp_file
                cmd = f'type "{temp_file}" | claude' if use_shell else f'claude < "{temp_file}"'
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=use_shell
                )
                
                stdout, stderr = process.communicate(timeout=90)
                
                if stdout and process.returncode == 0:
                    reply = stdout.strip()
                    # Extract just the reply (remove any Claude commentary)
                    if 'REPLY:' in reply:
                        reply = reply.split('REPLY:')[-1].strip()
                    self.logger.info(f'[OK] Claude reply: {reply[:100]}...')
                    return reply
            finally:
                # Clean up temp file
                try:
                    os.unlink(temp_file)
                except:
                    pass
            
        except subprocess.TimeoutExpired:
            self.logger.warning('Claude timeout (90s) - using fallback reply')
        except Exception as e:
            self.logger.warning(f'Claude error: {e}')
        
        # Fallback - generic but friendly
        return f"Hi,\n\nThanks for your email. I'll get back to you soon!\n\nBest"

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

    def create_plan(self, task_file: Path, objective: str, steps: List[str]) -> Path:
        """
        Create a Plan.md file for a task.
        
        Args:
            task_file: Original task file
            objective: Task objective
            steps: List of step descriptions
        
        Returns:
            Path: Path to created plan file
        """
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        plan_name = f'PLAN_{task_file.stem}_{timestamp}.md'
        plan_path = self.plans / plan_name
        
        # Build checklist
        checklist = '\n'.join([f'- [ ] {step}' for step in steps])
        
        content = f'''---
type: plan
source_task: {task_file.name}
created: {datetime.now().isoformat()}
status: in_progress
---

# Plan: {objective}

## Objective

{objective}

## Steps

{checklist}

## Notes

*Add any additional notes or context here.*

---
*Generated by AI Employee Orchestrator*
'''
        
        plan_path.write_text(content)
        self.logger.info(f'Created plan: {plan_name}')
        
        return plan_path
    
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
                [self.claude_command,],
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

        Complete flow:
        1. Detect approved file
        2. Update Plan status
        3. Execute action (LinkedIn post, email, etc.)
        4. Move to Done ONLY if successful

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

            # Determine action type and execute
            action_executed = False
            action_success = False
            action_type = 'generic'

            # Check if it's a LinkedIn post (multiple methods)
            is_linkedin = (
                'linkedin' in approved_file.name.lower() or
                'type: linkedin' in content.lower()
            )
            
            # If not found, check the source_task file
            if not is_linkedin:
                source_match = None
                for line in content.split('\n'):
                    if 'source_task:' in line:
                        source_match = line.split(':')[1].strip()
                        break
                
                if source_match:
                    source_file = self.pending_approval / source_match
                    if not source_file.exists():
                        source_file = self.needs_action / source_match
                    
                    if source_file.exists():
                        source_content = source_file.read_text(encoding='utf-8').lower()
                        if 'linkedin' in source_content:
                            is_linkedin = True
                            self.logger.info(f'[INFO] LinkedIn detected in source file: {source_match}')

            if is_linkedin:
                self.logger.info('Detected LinkedIn post action')
                action_type = 'linkedin'
                action_executed = True
                action_success = self._execute_linkedin_post(approved_file, content)

            # Check if it's an email
            elif 'email' in approved_file.name.lower() or 'type: email' in content.lower():
                self.logger.info('Detected email action')
                action_type = 'email'
                action_executed = True
                action_success = self._execute_email_send(approved_file, content)

            # Generic approval (just move to Done)
            else:
                self.logger.info('Generic approval - moving to Done')
                action_type = 'generic'
                action_executed = True
                action_success = True

            # Update Plan status
            self._update_plan_status(approved_file, action_success)

            # DON'T auto-move to Done for emails - user needs to confirm send
            # File stays in Approved/ until user manually moves it after sending
            if action_type != 'email' and action_success:
                dest = self.done / approved_file.name
                try:
                    shutil.move(str(approved_file), str(dest))
                    self.logger.info(f'[OK] Moved to Done: {approved_file.name}')
                    self.stats['tasks_completed'] += 1
                except Exception as e:
                    self.logger.error(f'Error moving to Done: {e}')
            elif action_type == 'email':
                # Email already sent via API - nothing more to do
                pass
            else:
                self.logger.error(f'[FAIL] Action failed - file remains in Approved/ for retry')

    def _check_email_sent(self, to_email: str, subject: str) -> bool:
        """
        Check if email was sent by checking Gmail Sent folder.
        Returns True if email found in Sent folder.
        """
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            
            # Load credentials (same as Gmail Watcher)
            token_path = Path(__file__).parent / 'watchers' / 'token.json'
            
            if not token_path.exists():
                self.logger.debug('[DEBUG] Gmail token not found')
                return False
            
            creds = Credentials.from_authorized_user_file(token_path)
            service = build('gmail', 'v1', credentials=creds)
            
            # Search Sent folder for recent emails to this recipient
            query = f'to:{to_email} subject:{subject}'
            results = service.users().messages().list(
                userId='me',
                labelIds=['SENT'],
                q=query,
                maxResults=5
            ).execute()
            
            messages = results.get('messages', [])
            
            if messages:
                # Check if any message is from last 2 minutes
                import time
                current_time = time.time()
                
                for msg in messages:
                    message = service.users().messages().get(
                        userId='me',
                        id=msg['id'],
                        format='metadata',
                        metadataHeaders=['Date']
                    ).execute()
                    
                    # Parse date
                    for header in message['payload']['headers']:
                        if header['name'] == 'Date':
                            from email.utils import parsedate_to_datetime
                            try:
                                msg_date = parsedate_to_datetime(header['value'])
                                msg_time = msg_date.timestamp()
                                
                                # If email was sent in last 2 minutes
                                if current_time - msg_time < 120:
                                    return True
                            except Exception as parse_error:
                                self.logger.debug(f'[DEBUG] Date parse error: {parse_error}')
                                pass
                
            return False
            
        except Exception as e:
            # Log but don't spam - network issues are common
            error_str = str(e)
            if 'oauth2' in error_str.lower() or 'server' in error_str.lower():
                self.logger.debug(f'[DEBUG] Gmail API network issue (will retry)')
            else:
                self.logger.warning(f'Could not check sent email: {e}')
            return False

    def _update_plan_status(self, approved_file: Path, success: bool):
        """
        Update the associated Plan.md status.
        """
        # Find associated plan
        source_task = approved_file.stem.replace('APPROVAL_', '')
        
        # Find most recent plan for this task
        plans = sorted(self.plans.glob(f'PLAN_{source_task}_*.md'), reverse=True)
        
        if plans:
            plan_file = plans[0]
            plan_content = plan_file.read_text()
            
            # Update status (using plain text, no emojis)
            if success:
                plan_content = plan_content.replace(
                    '## Status\nWaiting for approval...',
                    '## Status\nCOMPLETED - Action executed successfully'
                )
                # Mark all steps as done
                plan_content = plan_content.replace('- [ ]', '- [x]')
            else:
                plan_content = plan_content.replace(
                    '## Status\nWaiting for approval...',
                    '## Status\nFAILED - Action execution failed'
                )
            
            # Write with UTF-8 encoding
            plan_file.write_text(plan_content, encoding='utf-8')
            self.logger.info(f'[OK] Updated plan status: {plan_file.name}')

    def _execute_linkedin_post(self, approved_file: Path, content: str) -> bool:
        """
        Execute LinkedIn post via Playwright (direct browser automation).
        """
        self.logger.info('Executing LinkedIn post...')
        
        try:
            # Extract post content from original task file
            post_content = self._extract_post_content(content, approved_file)
            
            if not post_content or len(post_content) < 10:
                self.logger.error('[FAIL] No valid post content found')
                return False
            
            self.logger.info(f'[INFO] Post content: {post_content[:100]}...')
            
            # Use Playwright to post directly
            result = self._post_to_linkedin_direct(post_content)
            
            if result:
                self.logger.info('[OK] LinkedIn post executed successfully')
                self.log_operation('linkedin_post', {
                    'file': approved_file.name,
                    'content': post_content[:200],
                    'result': 'success'
                })
                return True
            else:
                self.logger.error('[FAIL] LinkedIn post failed - Browser automation error')
                return False
                
        except Exception as e:
            self.logger.error(f'Error executing LinkedIn post: {e}')
            return False

    def _post_to_linkedin_direct(self, post_content: str) -> bool:
        """
        Post to LinkedIn using Playwright directly.
        Uses the SAME session as LinkedIn Watcher for consistent authentication.
        """
        try:
            from playwright.sync_api import sync_playwright

            # Get session path - SAME as LinkedIn Watcher uses
            session_path = Path(__file__).parent / 'watchers' / 'linkedin_session'

            self.logger.info('[INFO] Opening LinkedIn with saved session...')
            self.logger.info(f'[INFO] Session path: {session_path}')

            # Check if session exists
            if not session_path.exists():
                self.logger.error('[FAIL] LinkedIn session not found!')
                self.logger.info('[INFO] Please run: python watchers/linkedin_watcher.py ../')
                self.logger.info('[INFO] Then login to LinkedIn')
                return False

            with sync_playwright() as p:
                # Launch browser with watcher's session - VISIBLE MODE
                browser = p.chromium.launch_persistent_context(
                    str(session_path),
                    headless=False,
                    args=[
                        '--disable-gpu',
                        '--disable-dev-shm-usage',
                        '--no-sandbox',
                        '--disable-blink-features=AutomationControlled'
                    ],
                    timeout=120000
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                # Navigate to LinkedIn home page
                self.logger.info('[INFO] Navigating to LinkedIn...')
                try:
                    page.goto('https://www.linkedin.com/', wait_until='domcontentloaded', timeout=30000)
                    import time
                    time.sleep(5)  # Wait for page to fully load
                except Exception as e:
                    self.logger.warning(f'Navigation warning: {e}')
                    # Continue anyway - page might still load

                # Check if logged in - look for multiple indicators
                self.logger.info('[INFO] Checking if logged in...')
                import time
                time.sleep(3)  # Let page settle
                
                def check_logged_in():
                    """Check if user is logged in using multiple methods."""
                    try:
                        # Method 1: Feed indicator
                        if page.query_selector('[aria-label="Feed"]'):
                            return True
                        # Method 2: Start a post button
                        if page.query_selector('button:has-text("Start a post")'):
                            return True
                        # Method 3: Me menu
                        if page.query_selector('[aria-label="Me"]'):
                            return True
                        # Method 4: Check URL (if we're on feed page, we're logged in)
                        if 'feed' in page.url or 'mynetwork' in page.url:
                            return True
                        # Method 5: Check for navigation bar
                        if page.query_selector('nav[aria-label="Primary Navigation"]'):
                            return True
                    except:
                        pass
                    return False

                is_logged_in = check_logged_in()

                if not is_logged_in:
                    self.logger.error('[FAIL] Not logged in to LinkedIn!')
                    self.logger.info('[INFO] Please login in the browser window NOW!')
                    self.logger.info('[INFO] Waiting 90 seconds for login...')
                    
                    for i in range(18):  # 90 seconds
                        time.sleep(5)
                        try:
                            is_logged_in = check_logged_in()
                            if is_logged_in:
                                self.logger.info('[OK] User logged in!')
                                time.sleep(3)  # Let page fully settle after login
                                break
                        except Exception as e:
                            # Page might be navigating, continue waiting
                            self.logger.debug(f'Waiting for login... ({i+1}/18)')
                            pass

                    if not is_logged_in:
                        self.logger.error('[FAIL] Login timeout - YOU MUST LOGIN WHEN BROWSER OPENS!')
                        self.logger.info('[INFO] Taking screenshot for debugging...')
                        try:
                            page.screenshot(path='linkedin_login_failed.png')
                            self.logger.info('[OK] Screenshot saved: linkedin_login_failed.png')
                        except:
                            pass
                        browser.close()
                        return False
                else:
                    self.logger.info('[OK] Already logged in!')

                self.logger.info('[INFO] Creating post...')

                # Wait for page to fully load
                import time
                time.sleep(3)

                # Click "Start a post" - try multiple methods
                post_clicked = False
                
                # Method 1: Click by text
                try:
                    start_post_btn = page.query_selector('button:has-text("Start a post")')
                    if start_post_btn:
                        start_post_btn.click()
                        self.logger.info('[OK] Post dialog opened (method 1)')
                        post_clicked = True
                except Exception as e:
                    self.logger.warning(f'Method 1 failed: {e}')
                
                # Method 2: Click by aria-label
                if not post_clicked:
                    try:
                        page.click('[aria-label="Start a post"]', timeout=5000)
                        self.logger.info('[OK] Post dialog opened (method 2)')
                        post_clicked = True
                    except Exception as e:
                        self.logger.warning(f'Method 2 failed: {e}')
                
                # Method 3: Click any button with "post" in text
                if not post_clicked:
                    try:
                        page.click('button:has-text("post")', timeout=5000)
                        self.logger.info('[OK] Post dialog opened (method 3)')
                        post_clicked = True
                    except Exception as e:
                        self.logger.warning(f'Method 3 failed: {e}')
                
                if not post_clicked:
                    self.logger.error('[FAIL] Could not open post dialog')
                    # Take screenshot for debugging
                    try:
                        page.screenshot(path='linkedin_post_error.png')
                        self.logger.info('[INFO] Screenshot saved: linkedin_post_error.png')
                    except:
                        pass
                    browser.close()
                    return False

                # Wait for dialog to appear
                self.logger.info('[INFO] Waiting for post dialog...')
                time.sleep(2)
                
                # Wait for textbox
                try:
                    page.wait_for_selector('[role="textbox"]', timeout=15000)
                    self.logger.info('[OK] Post dialog is ready')
                except Exception as e:
                    self.logger.warning(f'Dialog wait error: {e}')

                # Find editor and type content
                editor = page.query_selector('[role="textbox"]')
                if not editor:
                    editor = page.query_selector('div[contenteditable="true"]')
                
                if editor:
                    editor.fill(post_content)
                    self.logger.info('[OK] Post content entered')
                    time.sleep(2)
                else:
                    self.logger.error('[FAIL] Could not find editor')
                    browser.close()
                    return False

                # Wait and submit - multiple methods
                import time
                time.sleep(2)
                
                post_clicked = False
                
                # Method 1: Direct button click
                try:
                    post_button = page.query_selector('button:has-text("Post")')
                    if post_button:
                        post_button.click()
                        post_clicked = True
                        self.logger.info('[OK] Post submitted (method 1)')
                except Exception as e:
                    self.logger.warning(f'Method 1 failed: {e}')
                
                # Method 2: JavaScript click
                if not post_clicked:
                    try:
                        page.evaluate('''() => {
                            const buttons = document.querySelectorAll('button');
                            for (let btn of buttons) {
                                if (btn.textContent.includes('Post')) {
                                    btn.click();
                                    return true;
                                }
                            }
                            return false;
                        }''')
                        post_clicked = True
                        self.logger.info('[OK] Post submitted (method 2 - JS)')
                    except Exception as e:
                        self.logger.warning(f'Method 2 failed: {e}')
                
                # Method 3: Press Enter
                if not post_clicked:
                    try:
                        page.press('[role="textbox"]', 'Enter')
                        post_clicked = True
                        self.logger.info('[OK] Post submitted (method 3 - Enter)')
                    except Exception as e:
                        self.logger.warning(f'Method 3 failed: {e}')
                
                if post_clicked:
                    time.sleep(5)
                    self.logger.info('[OK] LinkedIn post completed!')
                    browser.close()
                    return True
                else:
                    self.logger.error('[FAIL] Could not submit post')
                    try:
                        page.screenshot(path='linkedin_submit_failed.png')
                    except:
                        pass
                    browser.close()
                    return False

        except ImportError:
            self.logger.error('Playwright not installed')
            return False
        except Exception as e:
            self.logger.error(f'LinkedIn posting error: {e}')
            return False

    def _execute_email_send(self, approved_file: Path, content: str) -> bool:
        """
        Execute email send:
        1. Extract reply draft from approval file
        2. Open Gmail in browser with reply
        3. User reviews and clicks Send
        4. Move to Done

        Args:
            approved_file: Path to approval file
            content: Content of the approval file

        Returns:
            bool: True if Gmail opened successfully
        """
        self.logger.info('Executing email send...')

        try:
            # Extract email details and reply draft
            email_from = ""
            email_subject = ""
            reply_body = ""
            gmail_id = ""
            in_draft = False
            draft_lines = []

            lines = content.split('\n')

            for i, line in enumerate(lines):
                line_lower = line.lower()

                # Extract FROM
                if 'from:' in line_lower and not email_from and 'type: email' not in line_lower:
                    email_from = line.split(':', 1)[1].strip()

                # Extract SUBJECT
                if 'subject:' in line_lower and not email_subject:
                    email_subject = line.split(':', 1)[1].strip()

                # Extract GMAIL_ID
                if 'gmail_id:' in line_lower:
                    gmail_id = line.split(':', 1)[1].strip()

                # Check for reply draft section
                if '## 📝 ai-generated reply draft' in line_lower or '## ai-generated reply draft' in line_lower:
                    in_draft = True
                    continue

                # Extract draft content (inside code blocks)
                if in_draft:
                    if line.strip().startswith('```'):
                        if draft_lines:  # End of code block
                            break
                        else:  # Start of code block
                            continue
                    elif line.strip():
                        draft_lines.append(line)

            # Join draft lines properly
            reply_body = '\n'.join(draft_lines).strip()

            # If no reply draft found, generate one
            if not reply_body.strip():
                self.logger.info('[INFO] No reply draft found, generating with Claude Code...')
                reply_body = self._generate_email_reply_for_approval(content)
            else:
                self.logger.info(f'[OK] Using existing reply draft ({len(reply_body)} chars)')

            if not email_from or not email_subject:
                self.logger.warning('Missing email details')
                return False

            self.logger.info(f'[INFO] Reply TO: {email_from}')
            self.logger.info(f'[INFO] Subject: Re: {email_subject}')
            self.logger.info(f'[INFO] Reply: {reply_body[:100]}...')

            # STEP 1: Open browser and login to Gmail (visible to user!)
            self.logger.info('[STEP 1] Opening Gmail in browser for login...')

            try:
                from playwright.sync_api import sync_playwright
                import time

                # Load Gmail ID for opening the original email
                gmail_id = ""
                for line in content.split('\n'):
                    if 'gmail_id:' in line.lower():
                        gmail_id = line.split(':', 1)[1].strip()
                        break

                with sync_playwright() as p:
                    # Use persistent Chrome profile
                    chrome_profile = Path(__file__).parent / 'watchers' / 'chrome_gmail_profile'
                    chrome_profile.mkdir(parents=True, exist_ok=True)

                    self.logger.info(f'[INFO] Chrome profile: {chrome_profile}')

                    # Launch browser with anti-detection
                    browser = p.chromium.launch_persistent_context(
                        user_data_dir=str(chrome_profile),
                        headless=False,
                        args=[
                            '--disable-blink-features=AutomationControlled',
                            '--disable-gpu',
                            '--no-sandbox',
                            '--start-maximized'
                        ],
                        ignore_default_args=['--enable-automation'],
                        timeout=120000
                    )

                    page = browser.pages[0] if browser.pages else browser.new_page()

                    # Hide automation
                    page.add_init_script('''
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                    ''')

                    # Go to Gmail
                    self.logger.info('[INFO] Please login to Gmail...')
                    self.logger.info('[INFO] You have 90 seconds to login...')
                    page.goto('https://mail.google.com/mail/u/0/', wait_until='domcontentloaded', timeout=90000)
                    page.wait_for_timeout(5000)

                    # Wait for login if needed
                    if 'accounts.google.com' in page.url or 'ServiceLogin' in page.url:
                        self.logger.info('[INFO] Waiting for login... (up to 90 seconds)')
                        try:
                            page.wait_for_url('**/mail.google.com/**', timeout=90000)
                        except:
                            self.logger.error('[FAIL] Login timeout!')
                            browser.close()
                            return False

                    self.logger.info('[OK] Logged in successfully!')
                    page.wait_for_timeout(2000)
                    
                    # If Gmail ID exists, open the original email
                    if gmail_id:
                        self.logger.info('[INFO] Opening original email...')
                        page.goto(f'https://mail.google.com/mail/u/0/#inbox/{gmail_id}')
                        page.wait_for_timeout(2000)

                        # Click Reply button
                        self.logger.info('[INFO] Clicking Reply button...')
                        try:
                            reply_button = page.query_selector('[aria-label="Reply"]')
                            if reply_button:
                                reply_button.click()
                                page.wait_for_timeout(2000)
                                self.logger.info('[OK] Reply opened!')
                            else:
                                page.click('[data-tooltip="Reply"]')
                                page.wait_for_timeout(2000)
                        except Exception as e:
                            self.logger.warning(f'Could not click reply: {e}')

                    # Type the reply
                    self.logger.info('[INFO] Typing reply...')
                    try:
                        textbox = page.query_selector('div[aria-label="Message Body"]')
                        if textbox:
                            textbox.click()
                            page.wait_for_timeout(500)

                            # Type the reply character by character
                            for char in reply_body[:300]:
                                textbox.type(char)
                                page.wait_for_timeout(50)

                            self.logger.info('[OK] Reply typed!')
                        else:
                            self.logger.error('[FAIL] Could not find reply textbox')
                            browser.close()
                            return False
                    except Exception as e:
                        self.logger.error(f'Error typing reply: {e}')
                        browser.close()
                        return False
                    
                    # Click Send button
                    self.logger.info('[INFO] Clicking Send button...')
                    page.wait_for_timeout(3000)

                    send_clicked = False

                    # Try Gmail's Send button
                    send_button = page.query_selector('button[jsname="b3eMjb"]')
                    if not send_button:
                        send_button = page.query_selector('[aria-label="Send"]')
                    if not send_button:
                        send_button = page.query_selector('button:has-text("Send")')

                    if send_button:
                        send_button.click()
                        send_clicked = True
                        self.logger.info('[OK] Send button clicked!')
                    else:
                        # JavaScript fallback
                        try:
                            page.evaluate('''() => {
                                const btns = document.querySelectorAll('button, div[role="button"]');
                                for (let btn of btns) {
                                    if (btn.textContent.includes('Send') || btn.getAttribute('aria-label') === 'Send') {
                                        btn.click();
                                        return true;
                                    }
                                }
                            }''')
                            send_clicked = True
                            self.logger.info('[OK] Send clicked via JavaScript')
                        except:
                            pass

                    if send_clicked:
                        page.wait_for_timeout(5000)
                        self.logger.info('[OK] Email sent!')
                        try:
                            page.screenshot(path='email_sent_confirmation.png')
                            self.logger.info('[OK] Screenshot saved')
                        except:
                            pass
                    else:
                        self.logger.error('[FAIL] Could not find Send button')
                        self.logger.info('[INFO] Please manually click Send')
                        page.wait_for_timeout(10000)
                        browser.close()
                        return False

                    # Show Sent folder
                    self.logger.info('[INFO] Opening Sent folder...')
                    page.goto('https://mail.google.com/mail/u/0/#sent')
                    page.wait_for_timeout(5000)

                    self.logger.info('[OK] Done! Email sent successfully!')
                    page.wait_for_timeout(3000)

                    browser.close()

                    # Move to Done
                    dest = self.done / approved_file.name
                    shutil.move(str(approved_file), str(dest))
                    self.logger.info(f'[OK] Moved to Done: {approved_file.name}')
                    self.stats['tasks_completed'] += 1

                    return True

            except ImportError:
                self.logger.error('[FAIL] Playwright not installed! Run: pip install playwright && playwright install')
                return False
            except Exception as send_error:
                self.logger.error(f'[FAIL] Email send error: {send_error}')
                # DON'T move file - let user retry
                return False

            # If we reach here, something went wrong
            self.logger.error('[FAIL] Email not sent - file remains in Approved/')
            return False

        except Exception as e:
            self.logger.error(f'Error executing email send: {e}')
            return False

    def _generate_email_reply(self, original_from: str, original_subject: str, email_content: str) -> str:
        """
        Generate a human-like email reply using Claude Code.
        Reads the actual email content and generates contextual reply.
        Uses temp file approach for reliable prompt passing.
        Timeout: 30 seconds max.
        """
        try:
            import subprocess
            import platform
            import tempfile
            import os

            # Extract email body from content
            email_body = ""
            in_body = False
            for line in email_content.split('\n'):
                if '## Email Content' in line:
                    in_body = True
                    continue
                if in_body:
                    if line.startswith('##') or line.startswith('---'):
                        break
                    email_body += line + '\n'

            # Simple prompt - reads actual email
            prompt_text = f"""Read this email and write a natural reply:

SUBJECT: {original_subject}
FROM: {original_from}
MESSAGE: {email_body[:300] if email_body else 'No message'}

Write a casual, human reply (1-3 sentences). No signatures. Just the reply text."""

            use_shell = platform.system() == 'Windows'

            # Create temp file with prompt
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(prompt_text)
                temp_file = f.name

            try:
                # Run: type temp_file | claude  (Windows) or claude < temp_file (Unix)
                cmd = f'type "{temp_file}" | claude' if use_shell else f'claude < "{temp_file}"'

                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=use_shell
                )

                stdout, stderr = process.communicate(timeout=30)

                if stdout and process.returncode == 0 and stdout.strip():
                    self.logger.info(f'[OK] Claude reply: {stdout[:100]}...')
                    return stdout.strip()
            finally:
                # Clean up temp file
                try:
                    os.unlink(temp_file)
                except:
                    pass

        except subprocess.TimeoutExpired:
            self.logger.warning('Claude timeout (30s)')
        except Exception as e:
            self.logger.warning(f'Claude error: {e}')

        # Fallback - generic but friendly
        return f"Hi,\n\nThanks for your email. I'll get back to you soon!\n\nBest"

    def _improve_reply_with_claude(self, subject: str, recipient: str, user_input: str) -> str:
        """
        Improve user's rough reply using Claude Code.
        Makes it professional, creative, and well-written.
        Uses temp file approach for reliable prompt passing.

        Args:
            subject: Email subject
            recipient: Email recipient
            user_input: User's rough reply input

        Returns:
            str: Improved reply
        """
        try:
            import subprocess
            import platform
            import tempfile
            import os

            # Prompt for Claude - improve user's input
            prompt_text = f"""You are a professional email communication assistant.

ORIGINAL EMAIL SUBJECT: {subject}
RECIPIENT: {recipient}

USER'S ROUGH REPLY (in Roman Urdu/Hindi):
```
{user_input}
```

TASK: Convert this to professional, warm English email reply:
1. Make it polite and friendly
2. Use simple, clear English
3. Keep it concise (2-4 sentences)
4. Fix grammar and spelling
5. Make it sound natural

Return ONLY the improved English reply (no explanations).

IMPROVED REPLY:"""

            use_shell = platform.system() == 'Windows'

            self.logger.info(f'[CLAUDE] Improving: {user_input[:50]}...')

            # Create temp file with prompt
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(prompt_text)
                temp_file = f.name

            try:
                # Run: type temp_file | claude  (Windows) or claude < temp_file (Unix)
                cmd = f'type "{temp_file}" | claude' if use_shell else f'claude < "{temp_file}"'

                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=use_shell
                )

                stdout, stderr = process.communicate(timeout=60)

                self.logger.info(f'[CLAUDE] stdout: {stdout[:200] if stdout else "EMPTY"}')
                self.logger.info(f'[CLAUDE] stderr: {stderr[:200] if stderr else "NONE"}')
                self.logger.info(f'[CLAUDE] returncode: {process.returncode}')

                if stdout and process.returncode == 0 and stdout.strip():
                    improved = stdout.strip()
                    self.logger.info(f'[OK] Claude improved reply: {improved[:100]}...')
                    return improved
                else:
                    self.logger.warning('[WARN] Claude returned empty/error - using simple improve')
            finally:
                # Clean up temp file
                try:
                    os.unlink(temp_file)
                except:
                    pass

        except subprocess.TimeoutExpired:
            self.logger.warning('Claude timeout (60s) - using fallback')
        except Exception as e:
            self.logger.warning(f'Claude error: {e}')

        # FALLBACK: Simple auto-improve (if Claude fails)
        return self._simple_improve_reply(user_input)

    def _simple_improve_reply(self, text: str) -> str:
        """
        Simple fallback to improve reply without Claude.
        Does basic cleanup and formatting.
        """
        text_lower = text.lower()
        
        # Complete Roman Urdu to English translations
        common_phrases = [
            ('iqra ko bolo', 'Tell Iqra'),
            ('iqra', 'Iqra'),
            ('main thek hon', "I'm doing well"),
            ('main thik hun', "I'm doing well"),
            ('main theek hun', "I'm doing well"),
            ('han', 'Yes'),
            ('haan', 'Yes'),
            ('han main', 'Yes, I'),
            ('kal hi', 'tomorrow'),
            ('kal', 'tomorrow'),
            ('tm sy milon ga', 'will meet you'),
            ('tum se milunga', 'will meet you'),
            ('tm', 'you'),
            ('tum', 'you'),
            ('tiems y ajana', 'please come at the time'),
            ('time pe ajana', 'please come on time'),
            ('same location py', 'at the same location'),
            ('same jagah', 'at the same place'),
            ('ok', 'Okay'),
            ('theek hai', 'Alright'),
            ('plx', 'Please'),
            ('please', 'Please'),
        ]
        
        improved = text_lower
        
        # Replace phrases (longer phrases first)
        for roman, english in common_phrases:
            improved = improved.replace(roman, english)
        
        # Clean up extra words
        cleanup = [
            ('ko bolo', ''),
            ('hi', ''),
            ('or', ''),
            ('aur', ''),
        ]
        for word, replacement in cleanup:
            improved = improved.replace(word, replacement)
        
        # Clean up extra spaces
        improved = ' '.join(improved.split())
        
        # Capitalize first letter
        improved = improved[0].upper() + improved[1:] if improved else ''
        
        # Add period if missing
        if improved and not improved.endswith(('.', '!', '?')):
            improved += '.'
        
        # If still looks like Roman Urdu, use generic reply
        if any(word in improved.lower() for word in ['main', 'tum', 'kal', 'mil', 'hon']):
            # Generic professional reply
            improved = "Hi! I'm doing well, thank you. Yes, I'd be happy to meet tomorrow. Please let me know the time and I'll be there at the same location. Looking forward to it!"
        
        self.logger.info(f'[FALLBACK] Simple improved: {improved[:100]}')
        return improved

    def _extract_post_content(self, content: str, task_file: Path = None) -> str:
        """Extract post content from approval file or original task file."""

        # Method 1: Look for "## Post Content" section
        lines = content.split('\n')
        post_lines = []
        in_post_section = False

        for line in lines:
            if '## Post Content' in line or '## LinkedIn Post' in line:
                in_post_section = True
                continue
            elif line.startswith('##') and in_post_section:
                break
            elif in_post_section and line.strip() and not line.startswith('---'):
                post_lines.append(line)

        if post_lines:
            result = '\n'.join(post_lines).strip()
            # Remove quotes if present
            if result.startswith('"') and result.endswith('"'):
                result = result[1:-1]
            if len(result) > 20:  # Valid content
                return result

        # Method 2: If this is an approval file, read the original task file
        if task_file and 'APPROVAL_' in task_file.name:
            # Find original file in Pending_Approval
            source_match = None
            for line in content.split('\n'):
                if 'source_task:' in line:
                    source_match = line.split(':')[1].strip()
                    break

            if source_match:
                original_file = self.pending_approval / source_match
                if original_file.exists():
                    original_content = original_file.read_text()
                    # Recursively extract from original
                    return self._extract_post_content(original_content, None)

        # Method 3: Look for original file in Inbox (by matching name)
        if task_file:
            # Try to find original inbox file
            for inbox_file in self.vault_path.glob('Inbox/*.md'):
                if inbox_file.stem in task_file.name or task_file.stem in inbox_file.name:
                    inbox_content = inbox_file.read_text()
                    result = self._extract_post_content(inbox_content, None)
                    if result and len(result) > 20:
                        return result

        # Fallback: return first 500 chars
        return content[:500] if content else ''

    def _extract_email_to(self, content: str) -> str:
        """Extract email recipient from content."""
        import re
        match = re.search(r'to:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        match = re.search(r'To:\s*(.+?)(?:\n|$)', content)
        if match:
            return match.group(1).strip()
        
        return ''

    def _extract_email_subject(self, content: str) -> str:
        """Extract email subject from content."""
        import re
        match = re.search(r'subject:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        match = re.search(r'Subject:\s*(.+?)(?:\n|$)', content)
        if match:
            return match.group(1).strip()
        
        return ''

    def _extract_email_body(self, content: str) -> str:
        """Extract email body from content."""
        lines = content.split('\n')
        body_lines = []
        in_body = False
        
        for line in lines:
            if '## Email Content' in line or '## Body' in line:
                in_body = True
                continue
            elif line.startswith('##') and in_body:
                break
            elif in_body:
                body_lines.append(line)
        
        if body_lines:
            return '\n'.join(body_lines).strip()
        
        return 'Email body not found'
    
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
    
    def run(self, poll_interval: int = 30, single_run: bool = True):
        """
        Main run loop.

        Args:
            poll_interval: Seconds between checks (default: 30)
            single_run: If True, process once and exit. If False, run continuously.
        """
        print("\n" + "=" * 60)
        print("🤖 AI Employee Orchestrator")
        print("=" * 60)

        try:
            # Process pending tasks
            pending_tasks = self.get_pending_tasks()

            if pending_tasks:
                print(f"📥 Found {len(pending_tasks)} pending task(s)\n")
                for task in pending_tasks:
                    self.process_task(task)
            else:
                print("✓ No pending tasks\n")

            # Process approved actions
            approved = self.get_approved_actions()
            if approved:
                print(f"📤 Found {len(approved)} approved action(s)\n")
                self.process_approved_actions()

            # Update stats
            self.stats['approvals_pending'] = len(self.get_approved_actions())

            # Final summary
            print("\n" + "=" * 60)
            print("📊 Summary")
            print("-" * 60)
            print(f"   Processed: {self.stats['tasks_processed']}")
            print(f"   Completed: {self.stats['tasks_completed']}")
            print(f"   Pending:   {self.stats['approvals_pending']}")
            print(f"   Errors:    {self.stats['errors']}")
            print("=" * 60 + "\n")

            if single_run:
                return

            # Continuous mode - keep running
            print("🕐 Continuous mode - waiting for tasks...\n")
            while True:
                time.sleep(poll_interval)

                # Process pending tasks
                pending_tasks = self.get_pending_tasks()
                if pending_tasks:
                    print(f"\n📥 Found {len(pending_tasks)} pending task(s)\n")
                    for task in pending_tasks:
                        self.process_task(task)

                # Process approved actions
                approved = self.get_approved_actions()
                if approved:
                    print(f"\n📤 Found {len(approved)} approved action(s)\n")
                    self.process_approved_actions()

                # Log periodic stats
                self.logger.debug(f'Stats: {self.stats}')

        except KeyboardInterrupt:
            print("\n\n⏹️  Orchestrator stopped by user\n")
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
        help='Seconds between checks (default: 30, only used in continuous mode)'
    )
    parser.add_argument(
        '--continuous',
        action='store_true',
        help='Run in continuous mode (default: single run)'
    )
    
    args = parser.parse_args()
    
    vault = Path(args.vault_path)
    if not vault.exists():
        print(f"Error: Vault path does not exist: {args.vault_path}")
        sys.exit(1)
    
    orchestrator = Orchestrator(str(vault), args.claude_command)
    
    # Run (single run by default, continuous if --continuous flag)
    orchestrator.run(args.poll_interval, single_run=not args.continuous)


if __name__ == '__main__':
    main()
