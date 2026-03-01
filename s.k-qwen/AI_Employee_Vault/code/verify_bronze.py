#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bronze Tier Verification Script

Run this script to verify that all Bronze Tier components are properly set up.

Usage:
    python verify_bronze.py
"""

import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import os
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')


def check(title: str, condition: bool, error_msg: str = ""):
    """Print check result."""
    if condition:
        print(f"[OK] {title}")
        return True
    else:
        print(f"[FAIL] {title}")
        if error_msg:
            print(f"  Error: {error_msg}")
        return False


def main():
    print("=" * 60)
    print("AI Employee - Bronze Tier Verification")
    print("=" * 60)
    print()
    
    vault_path = Path("AI_Employee_Vault")
    watchers_path = Path("watchers")
    
    all_passed = True
    
    # Check vault structure
    print("Vault Structure")
    print("-" * 40)
    
    required_folders = [
        "Inbox",
        "Needs_Action",
        "Done",
        "Plans",
        "Approved",
        "Pending_Approval",
        "Rejected",
        "Logs",
        "Accounting",
        "Briefings",
        "Invoices"
    ]
    
    for folder in required_folders:
        all_passed &= check(
            f"Folder: {folder}",
            (vault_path / folder).exists(),
            f"Run: mkdir {vault_path / folder}"
        )
    
    print()
    
    # Check required files
    print("Required Files")
    print("-" * 40)
    
    required_files = {
        "Dashboard.md": "Main status dashboard",
        "Company_Handbook.md": "Rules of engagement",
        "Business_Goals.md": "Objectives and metrics"
    }
    
    for filename, description in required_files.items():
        filepath = vault_path / filename
        all_passed &= check(
            f"{filename} ({description})",
            filepath.exists(),
            "File not created"
        )
    
    print()
    
    # Check watcher scripts
    print("Watcher Scripts")
    print("-" * 40)
    
    watcher_files = {
        "base_watcher.py": "Abstract base class",
        "filesystem_watcher.py": "File system monitor"
    }
    
    for filename, description in watcher_files.items():
        filepath = watchers_path / filename
        all_passed &= check(
            f"{filename} ({description})",
            filepath.exists(),
            "Script not created"
        )
    
    print()
    
    # Check orchestrator
    print("Orchestrator")
    print("-" * 40)
    
    all_passed &= check(
        "orchestrator.py (Master process)",
        Path("orchestrator.py").exists(),
        "Orchestrator not created"
    )
    
    print()
    
    # Check dependencies
    print("Python Dependencies")
    print("-" * 40)
    
    try:
        import watchdog
        check("watchdog (File system watching)", True)
    except ImportError:
        check("watchdog (File system watching)", False, "pip install watchdog")
        all_passed = False
    
    try:
        import yaml
        check("pyyaml (YAML parsing)", True)
    except ImportError:
        check("pyyaml (YAML parsing)", False, "pip install pyyaml")
        all_passed = False
    
    try:
        import colorama
        check("colorama (Colored output)", True)
    except ImportError:
        check("colorama (Colored output)", False, "pip install colorama")
        all_passed = False
    
    print()
    
    # Check Claude Code
    print("Claude Code")
    print("-" * 40)
    
    import subprocess
    try:
        result = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"[OK] Claude Code installed: {result.stdout.strip()[:50]}")
        else:
            print(f"[FAIL] Claude Code check failed")
            all_passed = False
    except FileNotFoundError:
        print("[FAIL] Claude Code not found")
        print("  Install: npm install -g @anthropic/claude-code")
        all_passed = False
    except subprocess.TimeoutExpired:
        print("[WARN] Claude Code check timed out")
        # Don't fail on timeout, might be slow
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("[SUCCESS] All Bronze Tier checks passed!")
        print()
        print("Next steps:")
        print("  1. Open AI_Employee_Vault in Obsidian")
        print("  2. Run: python watchers/filesystem_watcher.py AI_Employee_Vault")
        print("  3. Run: python orchestrator.py AI_Employee_Vault")
        print("  4. Drop a file into AI_Employee_Vault/Inbox/")
    else:
        print("[ERROR] Some checks failed. Please fix the issues above.")
        sys.exit(1)
    
    print("=" * 60)


if __name__ == "__main__":
    main()
