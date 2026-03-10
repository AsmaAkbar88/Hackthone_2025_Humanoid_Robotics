#!/usr/bin/env node
/**
 * Email MCP Server - Send emails via Gmail API
 * 
 * This MCP server provides email sending capabilities for the AI Employee.
 * It integrates with Gmail API to send, draft, and search emails.
 * 
 * Usage:
 *   node email-mcp.js
 * 
 * Setup:
 *   1. Download credentials.json from Google Cloud Console
 *   2. Run once to authenticate: node email-mcp.js --auth
 *   3. Use with Claude Code or other MCP clients
 * 
 * Environment Variables:
 *   GMAIL_CREDENTIALS: Path to credentials.json (default: ./credentials.json)
 *   GMAIL_TOKEN: Path to token.json (default: ./token.json)
 *   DRY_RUN: If true, only log emails without sending (default: false)
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { readFile, writeFile } from 'fs/promises';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { google } from 'googleapis';
import nodemailer from 'nodemailer';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Configuration
const CREDENTIALS_PATH = process.env.GMAIL_CREDENTIALS || join(__dirname, 'credentials.json');
const TOKEN_PATH = process.env.GMAIL_TOKEN || join(__dirname, 'token.json');
const DRY_RUN = process.env.DRY_RUN === 'true';

// OAuth2 Client
let oauth2Client;
let transporter;

/**
 * Load or create OAuth2 credentials
 */
async function loadCredentials() {
  try {
    const credentialsContent = await readFile(CREDENTIALS_PATH, 'utf-8');
    const credentials = JSON.parse(credentialsContent);
    
    oauth2Client = new google.auth.OAuth2(
      credentials.web.client_id,
      credentials.web.client_secret,
      credentials.web.redirect_uris[0]
    );
    
    // Load saved token
    try {
      const tokenContent = await readFile(TOKEN_PATH, 'utf-8');
      const token = JSON.parse(tokenContent);
      oauth2Client.setCredentials(token);
    } catch (err) {
      console.error('No token found. Please run: node email-mcp.js --auth');
      process.exit(1);
    }
    
    return true;
  } catch (err) {
    console.error(`Error loading credentials: ${err.message}`);
    console.error('Download credentials from: https://developers.google.com/gmail/api/quickstart/nodejs');
    return false;
  }
}

/**
 * Create Gmail transporter
 */
async function createTransporter() {
  if (!oauth2Client) {
    await loadCredentials();
  }
  
  transporter = nodemailer.createTransport({
    host: 'smtp.gmail.com',
    port: 465,
    secure: true,
    auth: {
      type: 'OAuth2',
      user: oauth2Client.credentials.email || process.env.GMAIL_USER,
      clientId: oauth2Client.credentials.client_id,
      clientSecret: oauth2Client.credentials.client_secret,
      refreshToken: oauth2Client.credentials.refresh_token,
      accessToken: await oauth2Client.getAccessToken().then(r => r.token),
    },
  });
}

/**
 * Send email
 */
async function sendEmail({ to, subject, body, cc, bcc, attachments }) {
  if (DRY_RUN) {
    console.log('[DRY RUN] Would send email to:', to);
    return { success: true, messageId: 'dry-run', message: 'Email not sent (DRY_RUN mode)' };
  }
  
  if (!transporter) {
    await createTransporter();
  }
  
  const mailOptions = {
    from: process.env.GMAIL_USER || oauth2Client.credentials.email,
    to: Array.isArray(to) ? to.join(', ') : to,
    subject,
    text: body,
    html: body.replace(/\n/g, '<br>'),
  };
  
  if (cc) mailOptions.cc = cc;
  if (bcc) mailOptions.bcc = bcc;
  if (attachments) mailOptions.attachments = attachments;
  
  try {
    const info = await transporter.sendMail(mailOptions);
    return { success: true, messageId: info.messageId };
  } catch (err) {
    // Handle token refresh
    if (err.responseCode === 401) {
      await createTransporter();
      const info = await transporter.sendMail(mailOptions);
      return { success: true, messageId: info.messageId };
    }
    throw err;
  }
}

/**
 * Create draft email
 */
async function createDraft({ to, subject, body, cc }) {
  if (!oauth2Client) {
    await loadCredentials();
  }
  
  const gmail = google.gmail({ version: 'v1', auth: oauth2Client });
  
  const rawMessage = [
    'From: ' + (process.env.GMAIL_USER || oauth2Client.credentials.email),
    'To: ' + (Array.isArray(to) ? to.join(', ') : to),
    cc ? 'Cc: ' + cc : '',
    'Subject: ' + subject,
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=utf-8',
    '',
    body.replace(/\n/g, '<br>')
  ].join('\n');
  
  const encodedMessage = Buffer.from(rawMessage)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
  
  try {
    const response = await gmail.users.drafts.create({
      userId: 'me',
      requestBody: {
        message: {
          raw: encodedMessage
        }
      }
    });
    
    return { success: true, draftId: response.data.id };
  } catch (err) {
    throw new Error(`Failed to create draft: ${err.message}`);
  }
}

/**
 * Search emails
 */
async function searchEmails({ query, maxResults = 10 }) {
  if (!oauth2Client) {
    await loadCredentials();
  }
  
  const gmail = google.gmail({ version: 'v1', auth: oauth2Client });
  
  try {
    const response = await gmail.users.messages.list({
      userId: 'me',
      q: query,
      maxResults
    });
    
    const messages = response.data.messages || [];
    const results = [];
    
    for (const msg of messages) {
      const fullMessage = await gmail.users.messages.get({
        userId: 'me',
        id: msg.id,
        format: 'metadata',
        metadataHeaders: ['From', 'To', 'Subject', 'Date']
      });
      
      const headers = fullMessage.data.payload.headers;
      results.push({
        id: msg.id,
        from: headers.find(h => h.name === 'From')?.value,
        to: headers.find(h => h.name === 'To')?.value,
        subject: headers.find(h => h.name === 'Subject')?.value,
        date: headers.find(h => h.name === 'Date')?.value
      });
    }
    
    return { success: true, emails: results };
  } catch (err) {
    throw new Error(`Failed to search emails: ${err.message}`);
  }
}

// MCP Server
const server = new Server(
  {
    name: 'email-mcp',
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
        name: 'send_email',
        description: 'Send an email via Gmail. Requires approval for sensitive actions.',
        inputSchema: {
          type: 'object',
          properties: {
            to: {
              type: 'string',
              description: 'Recipient email address (or comma-separated list)'
            },
            subject: {
              type: 'string',
              description: 'Email subject'
            },
            body: {
              type: 'string',
              description: 'Email body text'
            },
            cc: {
              type: 'string',
              description: 'CC recipients (comma-separated)'
            },
            bcc: {
              type: 'string',
              description: 'BCC recipients (comma-separated)'
            },
            attachments: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  filename: { type: 'string' },
                  path: { type: 'string' }
                }
              },
              description: 'Attachments to include'
            }
          },
          required: ['to', 'subject', 'body']
        }
      },
      {
        name: 'create_draft',
        description: 'Create a draft email without sending. Safe for review.',
        inputSchema: {
          type: 'object',
          properties: {
            to: {
              type: 'string',
              description: 'Recipient email address'
            },
            subject: {
              type: 'string',
              description: 'Email subject'
            },
            body: {
              type: 'string',
              description: 'Email body text'
            },
            cc: {
              type: 'string',
              description: 'CC recipients'
            }
          },
          required: ['to', 'subject', 'body']
        }
      },
      {
        name: 'search_emails',
        description: 'Search Gmail for emails matching query',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Gmail search query (e.g., "from:boss is:unread")'
            },
            maxResults: {
              type: 'number',
              description: 'Maximum results to return',
              default: 10
            }
          },
          required: ['query']
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
      case 'send_email':
        const sendResult = await sendEmail(args);
        return {
          content: [{ type: 'text', text: JSON.stringify(sendResult, null, 2) }]
        };
      
      case 'create_draft':
        const draftResult = await createDraft(args);
        return {
          content: [{ type: 'text', text: JSON.stringify(draftResult, null, 2) }]
        };
      
      case 'search_emails':
        const searchResult = await searchEmails(args);
        return {
          content: [{ type: 'text', text: JSON.stringify(searchResult, null, 2) }]
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
  const credentialsContent = await readFile(CREDENTIALS_PATH, 'utf-8');
  const credentials = JSON.parse(credentialsContent);

  // Support both 'web' and 'installed' formats
  const creds = credentials.web || credentials.installed;
  
  oauth2Client = new google.auth.OAuth2(
    creds.client_id,
    creds.client_secret,
    creds.redirect_uris[0]
  );
  
  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: ['https://www.googleapis.com/auth/gmail.send']
  });
  
  console.log('Authorize this app by visiting this url:', authUrl);
  console.log('Enter the code from the redirect page:');
  
  // Simple CLI input for code
  process.stdin.once('data', async (code) => {
    const codeStr = code.toString().trim();
    const { tokens } = await oauth2Client.getToken(codeStr);
    oauth2Client.setCredentials(tokens);
    
    await writeFile(TOKEN_PATH, JSON.stringify(tokens));
    console.log('Token saved to', TOKEN_PATH);
    process.exit(0);
  });
}

// Main
async function main() {
  if (process.argv.includes('--auth')) {
    await authenticate();
    return;
  }
  
  if (process.argv.includes('--check')) {
    const ok = await loadCredentials();
    console.log(ok ? 'Credentials OK' : 'Credentials missing');
    process.exit(ok ? 0 : 1);
    return;
  }
  
  // Load credentials
  await loadCredentials();
  await createTransporter();
  
  console.error('Email MCP Server running on stdio');
  
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});
