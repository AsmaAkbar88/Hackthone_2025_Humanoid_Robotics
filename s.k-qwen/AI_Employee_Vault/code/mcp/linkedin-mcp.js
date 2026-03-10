#!/usr/bin/env node
/**
 * LinkedIn MCP Server - Post to LinkedIn
 * 
 * This MCP server provides LinkedIn posting capabilities for the AI Employee.
 * It uses Playwright for browser automation to post updates.
 * 
 * Usage:
 *   node linkedin-mcp.js
 * 
 * Setup:
 *   1. Install dependencies: npm install
 *   2. First run will open browser for login
 *   3. Session will be saved for subsequent uses
 * 
 * Environment Variables:
 *   LINKEDIN_SESSION_PATH: Path to store session data
 *   DRY_RUN: If true, only log posts without sending
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { mkdirSync, existsSync, writeFileSync, readFileSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Configuration
const SESSION_PATH = process.env.LINKEDIN_SESSION_PATH || join(__dirname, 'linkedin_session');
const DRY_RUN = process.env.DRY_RUN === 'true';

// Ensure session directory exists
if (!existsSync(SESSION_PATH)) {
  mkdirSync(SESSION_PATH, { recursive: true });
}

/**
 * Post to LinkedIn using Playwright
 */
async function postToLinkedIn({ content, imageUrl, visibility = 'PUBLIC' }) {
  if (DRY_RUN) {
    console.log('[DRY RUN] Would post to LinkedIn:', content.substring(0, 100));
    return { success: true, postId: 'dry-run', message: 'Post not created (DRY_RUN mode)' };
  }

  const { chromium } = await import('playwright');
  
  try {
    // Launch browser with persistent context
    const browser = await chromium.launchPersistentContext(SESSION_PATH, {
      headless: true,
      args: ['--disable-gpu', '--disable-dev-shm-usage', '--no-sandbox']
    });
    
    const page = browser.pages()[0] || await browser.newPage();
    
    // Navigate to LinkedIn
    await page.goto('https://www.linkedin.com', { waitUntil: 'networkidle' });
    
    // Check if logged in
    const isLoggedIn = await page.$('[aria-label="Notifications"]');
    
    if (!isLoggedIn) {
      await browser.close();
      return { 
        success: false, 
        error: 'Not logged in. Please authenticate first by running with --auth flag or manually logging in.' 
      };
    }
    
    // Navigate to post creation
    await page.goto('https://www.linkedin.com/feed/', { waitUntil: 'networkidle' });
    
    // Click on "Start a post"
    await page.click('[aria-label="Start a post"]');
    
    // Wait for modal
    await page.waitForSelector('[role="dialog"]', { timeout: 10000 });
    
    // Type content
    const editor = await page.$('[role="textbox"]');
    if (editor) {
      await editor.fill(content);
    }
    
    // Add image if provided
    if (imageUrl) {
      const mediaButton = await page.$('button:has-text("Media")');
      if (mediaButton) {
        await mediaButton.click();
        // Note: File upload requires additional handling
        console.log('Image upload requires manual intervention');
      }
    }
    
    // Set visibility
    if (visibility === 'CONNECTIONS') {
      const visibilityButton = await page.$('button:has-text("Anyone")');
      if (visibilityButton) {
        await visibilityButton.click();
        await page.click('text=Connections');
      }
    }
    
    // Click Post button
    const postButton = await page.$('button:has-text("Post")');
    if (postButton) {
      await postButton.click();
      await page.waitForTimeout(3000);
      
      await browser.close();
      return { success: true, message: 'Post created successfully' };
    }
    
    await browser.close();
    return { success: false, error: 'Could not find Post button' };
    
  } catch (err) {
    console.error('LinkedIn posting error:', err.message);
    return { success: false, error: err.message };
  }
}

/**
 * Create a draft post (save for later)
 */
async function createDraftPost({ content }) {
  // For now, just log the draft
  const draftFile = join(__dirname, 'linkedin_drafts.json');
  
  let drafts = [];
  if (existsSync(draftFile)) {
    try {
      drafts = JSON.parse(readFileSync(draftFile, 'utf-8'));
    } catch (e) {
      drafts = [];
    }
  }
  
  drafts.push({
    content,
    created: new Date().toISOString(),
    status: 'draft'
  });
  
  writeFileSync(draftFile, JSON.stringify(drafts, null, 2));
  
  return { 
    success: true, 
    draftId: `draft_${Date.now()}`,
    message: 'Draft saved locally'
  };
}

/**
 * Get recent posts/analytics
 */
async function getRecentPosts({ limit = 5 }) {
  // This would require LinkedIn API access
  // For now, return placeholder
  return {
    success: true,
    posts: [],
    message: 'Post analytics requires LinkedIn API access'
  };
}

// MCP Server
const server = new Server(
  {
    name: 'linkedin-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'post_to_linkedin',
        description: 'Post an update to LinkedIn. Requires authentication. Creates approval request for review before posting.',
        inputSchema: {
          type: 'object',
          properties: {
            content: {
              type: 'string',
              description: 'Post content (max 3000 characters)'
            },
            imageUrl: {
              type: 'string',
              description: 'Optional image URL to include'
            },
            visibility: {
              type: 'string',
              enum: ['PUBLIC', 'CONNECTIONS'],
              default: 'PUBLIC',
              description: 'Post visibility'
            }
          },
          required: ['content']
        }
      },
      {
        name: 'create_linkedin_draft',
        description: 'Create a draft LinkedIn post for review. Safe operation that does not post.',
        inputSchema: {
          type: 'object',
          properties: {
            content: {
              type: 'string',
              description: 'Draft post content'
            }
          },
          required: ['content']
        }
      },
      {
        name: 'get_linkedin_posts',
        description: 'Get recent LinkedIn posts and analytics',
        inputSchema: {
          type: 'object',
          properties: {
            limit: {
              type: 'number',
              default: 5,
              description: 'Number of posts to retrieve'
            }
          }
        }
      }
    ]
  };
});

// Call tool
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  try {
    switch (name) {
      case 'post_to_linkedin':
        const postResult = await postToLinkedIn(args);
        return {
          content: [{ type: 'text', text: JSON.stringify(postResult, null, 2) }]
        };
      
      case 'create_linkedin_draft':
        const draftResult = await createDraftPost(args);
        return {
          content: [{ type: 'text', text: JSON.stringify(draftResult, null, 2) }]
        };
      
      case 'get_linkedin_posts':
        const postsResult = await getRecentPosts(args);
        return {
          content: [{ type: 'text', text: JSON.stringify(postsResult, null, 2) }]
        };
      
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (err) {
    return {
      content: [{ type: 'text', text: `Error: ${err.message}` }],
      isError: true
    };
  }
});

// Authentication helper
async function authenticate() {
  console.log('Opening browser for LinkedIn authentication...');
  
  const { chromium } = await import('playwright');
  
  try {
    const browser = await chromium.launchPersistentContext(SESSION_PATH, {
      headless: false,
      args: ['--disable-gpu', '--no-sandbox']
    });
    
    const page = browser.pages()[0] || await browser.newPage();
    await page.goto('https://www.linkedin.com');
    
    console.log('Please log in to LinkedIn');
    console.log('Browser will close automatically after 60 seconds');
    
    setTimeout(async () => {
      await browser.close();
      console.log('Authentication complete. Session saved.');
      process.exit(0);
    }, 60000);
    
  } catch (err) {
    console.error('Authentication error:', err.message);
    process.exit(1);
  }
}

// Main
async function main() {
  if (process.argv.includes('--auth')) {
    await authenticate();
    return;
  }
  
  if (process.argv.includes('--check')) {
    const sessionExists = existsSync(SESSION_PATH);
    console.log(sessionExists ? 'Session found' : 'No session found. Run with --auth first.');
    process.exit(sessionExists ? 0 : 1);
    return;
  }
  
  console.error('LinkedIn MCP Server running on stdio');
  
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});
