#!/usr/bin/env npx tsx
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { BrowserStackClient } from './client.js';
import type { BrowserStackSessionUpdate } from './types.js';

const config = {
  username: process.env.BROWSERSTACK_USERNAME ?? '',
  accessKey: process.env.BROWSERSTACK_ACCESS_KEY ?? '',
};

if (!config.username || !config.accessKey) {
  console.error(
    'Missing BrowserStack configuration. Set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY.',
  );
  process.exit(1);
}

const client = new BrowserStackClient(config);

const server = new Server(
  { name: 'pw-browserstack', version: '1.0.0' },
  { capabilities: { tools: {} } },
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'browserstack_get_plan',
      description: 'Get BrowserStack Automate plan details including parallel session limits',
      inputSchema: { type: 'object', properties: {} },
    },
    {
      name: 'browserstack_get_browsers',
      description: 'List all available browser and OS combinations for Playwright testing',
      inputSchema: { type: 'object', properties: {} },
    },
    {
      name: 'browserstack_get_builds',
      description: 'List recent test builds with status',
      inputSchema: {
        type: 'object',
        properties: {
          limit: { type: 'number', description: 'Max builds to return (default 10)' },
          status: {
            type: 'string',
            enum: ['running', 'done', 'failed', 'timeout'],
            description: 'Filter by status',
          },
        },
      },
    },
    {
      name: 'browserstack_get_sessions',
      description: 'List test sessions within a build',
      inputSchema: {
        type: 'object',
        properties: {
          build_id: { type: 'string', description: 'Build hashed ID' },
          limit: { type: 'number', description: 'Max sessions to return' },
        },
        required: ['build_id'],
      },
    },
    {
      name: 'browserstack_get_session',
      description: 'Get detailed session info including video URL, logs, and screenshots',
      inputSchema: {
        type: 'object',
        properties: {
          session_id: { type: 'string', description: 'Session hashed ID' },
        },
        required: ['session_id'],
      },
    },
    {
      name: 'browserstack_update_session',
      description: 'Update session status (mark as passed/failed) and name',
      inputSchema: {
        type: 'object',
        properties: {
          session_id: { type: 'string', description: 'Session hashed ID' },
          status: {
            type: 'string',
            enum: ['passed', 'failed'],
            description: 'Test result status',
          },
          name: { type: 'string', description: 'Updated session name' },
          reason: { type: 'string', description: 'Reason for failure' },
        },
        required: ['session_id'],
      },
    },
    {
      name: 'browserstack_get_logs',
      description: 'Get text logs for a specific test session',
      inputSchema: {
        type: 'object',
        properties: {
          session_id: { type: 'string', description: 'Session hashed ID' },
        },
        required: ['session_id'],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'browserstack_get_plan': {
        const plan = await client.getPlan();
        return { content: [{ type: 'text', text: JSON.stringify(plan, null, 2) }] };
      }

      case 'browserstack_get_browsers': {
        const browsers = await client.getBrowsers();
        const playwrightBrowsers = browsers.filter(
          (b) =>
            ['chrome', 'firefox', 'playwright-chromium', 'playwright-firefox', 'playwright-webkit'].includes(
              b.browser?.toLowerCase() ?? '',
            ) || b.browser?.toLowerCase().includes('playwright'),
        );
        const summary = playwrightBrowsers.length > 0 ? playwrightBrowsers : browsers.slice(0, 50);
        return { content: [{ type: 'text', text: JSON.stringify(summary, null, 2) }] };
      }

      case 'browserstack_get_builds': {
        const builds = await client.getBuilds(
          (args?.limit as number) ?? 10,
          args?.status as string | undefined,
        );
        return { content: [{ type: 'text', text: JSON.stringify(builds, null, 2) }] };
      }

      case 'browserstack_get_sessions': {
        const sessions = await client.getSessions(
          args!.build_id as string,
          args?.limit as number | undefined,
        );
        return { content: [{ type: 'text', text: JSON.stringify(sessions, null, 2) }] };
      }

      case 'browserstack_get_session': {
        const session = await client.getSession(args!.session_id as string);
        return { content: [{ type: 'text', text: JSON.stringify(session, null, 2) }] };
      }

      case 'browserstack_update_session': {
        const update: BrowserStackSessionUpdate = {};
        if (args?.status) update.status = args.status as 'passed' | 'failed';
        if (args?.name) update.name = args.name as string;
        if (args?.reason) update.reason = args.reason as string;
        const updated = await client.updateSession(args!.session_id as string, update);
        return { content: [{ type: 'text', text: JSON.stringify(updated, null, 2) }] };
      }

      case 'browserstack_get_logs': {
        const logs = await client.getSessionLogs(args!.session_id as string);
        return { content: [{ type: 'text', text: logs }] };
      }

      default:
        return { content: [{ type: 'text', text: `Unknown tool: ${name}` }], isError: true };
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return { content: [{ type: 'text', text: `Error: ${message}` }], isError: true };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
