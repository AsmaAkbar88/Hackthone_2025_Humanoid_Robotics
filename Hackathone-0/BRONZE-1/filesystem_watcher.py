# filesystem_watcher.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import shutil
import time
from base_watcher import BaseWatcher

class InboxFolderHandler(FileSystemEventHandler):
    def __init__(self, vault_path: str, inbox_folder: str):
        self.inbox = Path(inbox_folder)
        self.needs_action = Path(vault_path) / 'Needs_Action'
        # Create the inbox folder if it doesn't exist
        self.inbox.mkdir(exist_ok=True)

    def on_created(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)
        # Process only .md files, ignore other formats
        try:
            if source.suffix.lower() == '.md':
                # For .md files, move them directly to Needs_Action for processing
                dest = self.needs_action / source.name
                shutil.move(str(source), str(dest))
                print(f"File {source.name} moved from Inbox to Needs_Action for processing.")
            else:
                # For non-md files, ignore them (don't process)
                print(f"Ignoring non-md file: {source.name}")
        except Exception as e:
            print(f"Error processing file {source.name}: {e}")

    def on_moved(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)
        # Process only .md files, ignore other formats
        try:
            if source.suffix.lower() == '.md':
                # For .md files, move them directly to Needs_Action for processing
                dest = self.needs_action / source.name
                shutil.move(str(source), str(dest))
                print(f"File {source.name} moved from Inbox to Needs_Action for processing.")
            else:
                # For non-md files, ignore them (don't process)
                print(f"Ignoring non-md file: {source.name}")
        except Exception as e:
            print(f"Error processing file {source.name}: {e}")

    def create_metadata_with_content(self, meta_path: Path, source_name: str, file_content: str):
        # Calculate file size from the content
        original_size = len(file_content.encode('utf-8'))

        meta_path.write_text(f'''---
type: inbox_file
original_name: {source_name}
size: {original_size}
detected: {time.strftime("%Y-%m-%d %H:%M:%S")}
---
# New File in Inbox for Processing

A new file has arrived in the Inbox and needs processing:

- **File Name**: {source_name}
- **Size**: {original_size} bytes
- **Action Required**: Review and process this file from Inbox

## Original File Content
```
{file_content}
```

## Processing Steps
- [ ] Review file content
- [ ] Determine appropriate action
- [ ] Process file as needed
- [ ] Update status when complete
''')

    def create_metadata(self, meta_path: Path, source_name: str):
        # Fallback method for backward compatibility if needed
        # Get the size of the original file that was moved
        original_file_path = meta_path.with_suffix('')  # Remove .md to get the original file
        if original_file_path.exists():
            original_size = original_file_path.stat().st_size
        else:
            original_size = 0  # Fallback if original file doesn't exist yet

        meta_path.write_text(f'''---
type: inbox_file
original_name: {source_name}
size: {original_size}
detected: {time.strftime("%Y-%m-%d %H:%M:%S")}
---
# New File in Inbox for Processing

A new file has arrived in the Inbox and needs processing:

- **File Name**: {source_name}
- **Size**: {original_size} bytes
- **Action Required**: Review and process this file from Inbox

## Processing Steps
- [ ] Review file content
- [ ] Determine appropriate action
- [ ] Process file as needed
- [ ] Update status when complete
''')

class FileSystemWatcher(BaseWatcher):
    def __init__(self, vault_path: str, inbox_folder: str = None):
        super().__init__(vault_path, check_interval=10)  # Check every 10 seconds
        self.inbox = Path(inbox_folder) if inbox_folder else Path(vault_path) / 'Inbox'
        self.handler = InboxFolderHandler(vault_path, str(self.inbox))
        self.observer = Observer()
        self.observer.schedule(self.handler, str(self.inbox), recursive=False)

    def check_for_updates(self) -> list:
        # For the file system watcher, we rely on the event handler
        # rather than polling, so this can be a simple check
        return []

    def create_action_file(self, item) -> Path:
        # This is handled by the event handler
        pass

    def run(self):
        self.logger.info(f'Starting FileSystemWatcher for {self.inbox}')
        self.needs_action.mkdir(exist_ok=True)  # Ensure Needs_Action directory exists
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("FileSystemWatcher stopped by user.")
        finally:
            self.observer.join()