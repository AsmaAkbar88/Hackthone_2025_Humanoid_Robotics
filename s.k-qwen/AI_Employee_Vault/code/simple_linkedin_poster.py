#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple LinkedIn Poster - Fully Automatic
Posts to LinkedIn automatically with user's help during first login.
"""

import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Playwright not installed. Run: pip install playwright && playwright install")
    sys.exit(1)


def post_to_linkedin(post_content: str, session_path: str) -> bool:
    """
    Post to LinkedIn automatically.
    
    Args:
        post_content: Content to post
        session_path: Path to store browser session
    
    Returns:
        bool: True if successful
    """
    print(f'[INFO] Opening LinkedIn...')
    
    with sync_playwright() as p:
        # Launch browser with persistent session
        browser = p.chromium.launch_persistent_context(
            session_path,
            headless=False,  # Visible so user can see
            args=['--disable-gpu', '--no-sandbox'],
            timeout=120000
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        # Go to LinkedIn
        print('[INFO] Navigating to LinkedIn...')
        page.goto('https://www.linkedin.com/', wait_until='domcontentloaded', timeout=60000)
        time.sleep(5)
        
        # Check if logged in
        is_logged_in = page.query_selector('[aria-label="Feed"]') is not None
        
        if not is_logged_in:
            print('[INFO] Please login to LinkedIn in the browser window...')
            print('[INFO] Waiting 90 seconds...')
            
            for i in range(18):  # 90 seconds
                time.sleep(5)
                is_logged_in = page.query_selector('[aria-label="Feed"]') is not None
                if is_logged_in:
                    print('[OK] Logged in!')
                    break
            
            if not is_logged_in:
                print('[FAIL] Login timeout!')
                browser.close()
                return False
        
        # Create post
        print('[INFO] Creating post...')
        
        # Click "Start a post"
        try:
            page.click('button:has-text("Start a post")')
            print('[OK] Post dialog opened')
            time.sleep(2)
        except Exception as e:
            print(f'[FAIL] Could not open post dialog: {e}')
            browser.close()
            return False
        
        # Type content
        editor = page.query_selector('[role="textbox"]')
        if editor:
            editor.fill(post_content)
            print('[OK] Content typed')
            time.sleep(2)
        else:
            print('[FAIL] Could not find editor')
            browser.close()
            return False
        
        # Click Post button
        post_btn = page.query_selector('button:has-text("Post")')
        if post_btn:
            post_btn.click()
            print('[OK] Post button clicked!')
            time.sleep(5)
            print('[OK] LinkedIn post submitted successfully!')
        else:
            print('[FAIL] Post button not found')
            browser.close()
            return False
        
        browser.close()
        return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python simple_linkedin_poster.py <post_content>")
        sys.exit(1)
    
    post_content = ' '.join(sys.argv[1:])
    session_path = str(Path(__file__).parent / 'watchers' / 'linkedin_session')
    
    success = post_to_linkedin(post_content, session_path)
    sys.exit(0 if success else 1)
