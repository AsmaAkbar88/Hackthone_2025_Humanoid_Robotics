# vault_interaction_demo.py
"""
This script demonstrates how Claude Code can read from and write to the vault.
In a real implementation, Claude would use its built-in file system tools to read and write files directly.
"""

import json
from pathlib import Path
import datetime

def process_needs_action_folder(vault_path):
    """Simulate Claude processing files in the Needs_Action folder."""
    vault_path = Path(vault_path)
    needs_action_path = vault_path / "Needs_Action"

    print(f"Processing files in {needs_action_path}")

    # Find all markdown files in Needs_Action
    task_files = list(needs_action_path.glob("*.md"))

    if not task_files:
        print("No files to process in Needs_Action folder.")
        return

    for task_file in task_files:
        print(f"\nProcessing: {task_file.name}")

        # Read the task file
        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"Content preview: {content[:200]}...")

        # Simulate processing the task
        process_task(task_file, vault_path)

def process_task(task_file, vault_path):
    """Process an individual task file."""
    # Read the task content
    with open(task_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update Dashboard.md with latest information
    update_dashboard(vault_path)

    # After processing, move the task to Done folder
    done_path = vault_path / "Done"
    done_path.mkdir(exist_ok=True)  # Create Done folder if it doesn't exist

    # Create a processed version of the task
    processed_content = f"""{content}

---

## Processing Notes
- **Processed by**: Claude Code
- **Processing time**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Status**: Completed
- **Action**: Moved to Done folder

## Original Task Status
This task has been processed and completed.
"""

    # Write the processed task to the Done folder
    done_file = done_path / task_file.name
    with open(done_file, 'w', encoding='utf-8') as f:
        f.write(processed_content)

    print(f"Task processed and moved to Done: {done_file.name}")

def update_dashboard(vault_path):
    """Update the Dashboard.md file with current status."""
    dashboard_path = vault_path / "Dashboard.md"

    if dashboard_path.exists():
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            current_content = f.read()

    # Count files in different folders
    needs_action_count = len(list((vault_path / "Needs_Action").glob("*.md")))
    done_count = len(list((vault_path / "Done").glob("*.md")))

    # Update the dashboard content
    lines = current_content.split('\n')
    updated_lines = []

    for line in lines:
        if line.startswith('- Pending Messages'):
            # Update pending messages count with actual needs action count
            updated_lines.append(f'- Pending Messages: {needs_action_count}')
        elif line.startswith('- Completed Today'):
            # Update completed count
            updated_lines.append(f'- Completed Today: {done_count}')
        elif line.startswith('**Last Updated:**'):
            # Update timestamp
            updated_lines.append(f'**Last Updated:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        elif line.startswith('- Last Activity:'):
            # Update last activity
            updated_lines.append(f'- Last Activity: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        else:
            updated_lines.append(line)

    updated_content = '\n'.join(updated_lines)

    # Write updated content back to dashboard
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("Dashboard.md updated with current status.")

def main():
    vault_path = Path(".")
    print("AI Employee Vault Interaction Demo")
    print("==================================")

    # Process any tasks in Needs_Action
    process_needs_action_folder(vault_path)

    print("\nVault processing completed!")
    print("- Dashboard.md has been updated")
    print("- Tasks in Needs_Action have been processed")
    print("- Completed tasks moved to Done folder")

if __name__ == "__main__":
    main()