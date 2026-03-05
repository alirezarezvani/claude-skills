#!/usr/bin/env npx tsx
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { TestRailClient } from './client.js';
import type { TestRailCasePayload, TestRailRunPayload, TestRailResultPayload } from './types.js';

const config = {
  url: process.env.TESTRAIL_URL ?? '',
  user: process.env.TESTRAIL_USER ?? '',
  apiKey: process.env.TESTRAIL_API_KEY ?? '',
};

if (!config.url || !config.user || !config.apiKey) {
  console.error(
    'Missing TestRail configuration. Set TESTRAIL_URL, TESTRAIL_USER, and TESTRAIL_API_KEY.',
  );
  process.exit(1);
}

const client = new TestRailClient(config);

const server = new Server(
  { name: 'pw-testrail', version: '1.0.0' },
  { capabilities: { tools: {} } },
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'testrail_get_projects',
      description: 'List all TestRail projects',
      inputSchema: { type: 'object', properties: {} },
    },
    {
      name: 'testrail_get_suites',
      description: 'List test suites in a project',
      inputSchema: {
        type: 'object',
        properties: {
          project_id: { type: 'number', description: 'Project ID' },
        },
        required: ['project_id'],
      },
    },
    {
      name: 'testrail_get_cases',
      description: 'Get test cases from a project. Supports filtering by suite, section, and search text.',
      inputSchema: {
        type: 'object',
        properties: {
          project_id: { type: 'number', description: 'Project ID' },
          suite_id: { type: 'number', description: 'Suite ID (optional)' },
          section_id: { type: 'number', description: 'Section ID (optional)' },
          limit: { type: 'number', description: 'Max results (default 250)' },
          offset: { type: 'number', description: 'Offset for pagination' },
          filter: { type: 'string', description: 'Search text filter' },
        },
        required: ['project_id'],
      },
    },
    {
      name: 'testrail_add_case',
      description: 'Create a new test case in a section',
      inputSchema: {
        type: 'object',
        properties: {
          section_id: { type: 'number', description: 'Section ID to add the case to' },
          title: { type: 'string', description: 'Test case title' },
          template_id: { type: 'number', description: 'Template ID (2 = Test Case Steps)' },
          priority_id: { type: 'number', description: 'Priority (1=Low, 2=Medium, 3=High, 4=Critical)' },
          custom_preconds: { type: 'string', description: 'Preconditions text' },
          custom_steps_separated: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                content: { type: 'string', description: 'Step action' },
                expected: { type: 'string', description: 'Expected result' },
              },
            },
            description: 'Test steps with expected results',
          },
        },
        required: ['section_id', 'title'],
      },
    },
    {
      name: 'testrail_update_case',
      description: 'Update an existing test case',
      inputSchema: {
        type: 'object',
        properties: {
          case_id: { type: 'number', description: 'Case ID to update' },
          title: { type: 'string', description: 'Updated title' },
          custom_preconds: { type: 'string', description: 'Updated preconditions' },
          custom_steps_separated: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                content: { type: 'string' },
                expected: { type: 'string' },
              },
            },
            description: 'Updated test steps',
          },
        },
        required: ['case_id'],
      },
    },
    {
      name: 'testrail_add_run',
      description: 'Create a new test run in a project',
      inputSchema: {
        type: 'object',
        properties: {
          project_id: { type: 'number', description: 'Project ID' },
          name: { type: 'string', description: 'Run name' },
          description: { type: 'string', description: 'Run description' },
          suite_id: { type: 'number', description: 'Suite ID' },
          include_all: { type: 'boolean', description: 'Include all cases (default true)' },
          case_ids: {
            type: 'array',
            items: { type: 'number' },
            description: 'Specific case IDs to include (if include_all is false)',
          },
        },
        required: ['project_id', 'name'],
      },
    },
    {
      name: 'testrail_add_result',
      description: 'Add a test result for a specific case in a run',
      inputSchema: {
        type: 'object',
        properties: {
          run_id: { type: 'number', description: 'Run ID' },
          case_id: { type: 'number', description: 'Case ID' },
          status_id: {
            type: 'number',
            description: 'Status: 1=Passed, 2=Blocked, 3=Untested, 4=Retest, 5=Failed',
          },
          comment: { type: 'string', description: 'Result comment or error message' },
          elapsed: { type: 'string', description: 'Time spent (e.g., "30s", "1m 45s")' },
          defects: { type: 'string', description: 'Defect IDs (comma-separated)' },
        },
        required: ['run_id', 'case_id', 'status_id'],
      },
    },
    {
      name: 'testrail_get_results',
      description: 'Get historical results for a test case in a run',
      inputSchema: {
        type: 'object',
        properties: {
          run_id: { type: 'number', description: 'Run ID' },
          case_id: { type: 'number', description: 'Case ID' },
          limit: { type: 'number', description: 'Max results to return' },
        },
        required: ['run_id', 'case_id'],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'testrail_get_projects': {
        const projects = await client.getProjects();
        return { content: [{ type: 'text', text: JSON.stringify(projects, null, 2) }] };
      }

      case 'testrail_get_suites': {
        const suites = await client.getSuites(args!.project_id as number);
        return { content: [{ type: 'text', text: JSON.stringify(suites, null, 2) }] };
      }

      case 'testrail_get_cases': {
        const cases = await client.getCases(
          args!.project_id as number,
          args?.suite_id as number | undefined,
          args?.section_id as number | undefined,
          args?.limit as number | undefined,
          args?.offset as number | undefined,
          args?.filter as string | undefined,
        );
        return { content: [{ type: 'text', text: JSON.stringify(cases, null, 2) }] };
      }

      case 'testrail_add_case': {
        const payload: TestRailCasePayload = {
          title: args!.title as string,
          template_id: args?.template_id as number | undefined,
          priority_id: args?.priority_id as number | undefined,
          custom_preconds: args?.custom_preconds as string | undefined,
          custom_steps_separated: args?.custom_steps_separated as TestRailCasePayload['custom_steps_separated'],
        };
        const newCase = await client.addCase(args!.section_id as number, payload);
        return { content: [{ type: 'text', text: JSON.stringify(newCase, null, 2) }] };
      }

      case 'testrail_update_case': {
        const updatePayload: Partial<TestRailCasePayload> = {};
        if (args?.title) updatePayload.title = args.title as string;
        if (args?.custom_preconds) updatePayload.custom_preconds = args.custom_preconds as string;
        if (args?.custom_steps_separated) {
          updatePayload.custom_steps_separated = args.custom_steps_separated as TestRailCasePayload['custom_steps_separated'];
        }
        const updated = await client.updateCase(args!.case_id as number, updatePayload);
        return { content: [{ type: 'text', text: JSON.stringify(updated, null, 2) }] };
      }

      case 'testrail_add_run': {
        const runPayload: TestRailRunPayload = {
          name: args!.name as string,
          description: args?.description as string | undefined,
          suite_id: args?.suite_id as number | undefined,
          include_all: (args?.include_all as boolean) ?? true,
          case_ids: args?.case_ids as number[] | undefined,
        };
        const run = await client.addRun(args!.project_id as number, runPayload);
        return { content: [{ type: 'text', text: JSON.stringify(run, null, 2) }] };
      }

      case 'testrail_add_result': {
        const resultPayload: TestRailResultPayload = {
          status_id: args!.status_id as number,
          comment: args?.comment as string | undefined,
          elapsed: args?.elapsed as string | undefined,
          defects: args?.defects as string | undefined,
        };
        const result = await client.addResultForCase(
          args!.run_id as number,
          args!.case_id as number,
          resultPayload,
        );
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
      }

      case 'testrail_get_results': {
        const results = await client.getResultsForCase(
          args!.run_id as number,
          args!.case_id as number,
          args?.limit as number | undefined,
        );
        return { content: [{ type: 'text', text: JSON.stringify(results, null, 2) }] };
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
