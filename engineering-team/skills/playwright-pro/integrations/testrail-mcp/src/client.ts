import type {
  TestRailConfig,
  TestRailProject,
  TestRailSuite,
  TestRailCase,
  TestRailCasePayload,
  TestRailRun,
  TestRailRunPayload,
  TestRailResult,
  TestRailResultPayload,
} from './types.js';

export class TestRailClient {
  private readonly baseUrl: string;
  private readonly headers: Record<string, string>;

  constructor(config: TestRailConfig) {
    this.baseUrl = config.url.replace(/\/+$/, '');
    const auth = Buffer.from(`${config.user}:${config.apiKey}`).toString('base64');
    this.headers = {
      Authorization: `Basic ${auth}`,
      'Content-Type': 'application/json',
    };
  }

  private async request<T>(
    method: string,
    endpoint: string,
    body?: unknown,
  ): Promise<T> {
    const url = `${this.baseUrl}/index.php?/api/v2/${endpoint}`;
    const options: RequestInit = {
      method,
      headers: this.headers,
    };
    if (body) {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `TestRail API error ${response.status}: ${errorText}`,
      );
    }

    return response.json() as Promise<T>;
  }

  async getProjects(): Promise<TestRailProject[]> {
    const result = await this.request<{ projects: TestRailProject[] }>(
      'GET',
      'get_projects',
    );
    return result.projects ?? result as unknown as TestRailProject[];
  }

  async getSuites(projectId: number): Promise<TestRailSuite[]> {
    return this.request<TestRailSuite[]>('GET', `get_suites/${projectId}`);
  }

  async getCases(
    projectId: number,
    suiteId?: number,
    sectionId?: number,
    limit?: number,
    offset?: number,
    filter?: string,
  ): Promise<TestRailCase[]> {
    let endpoint = `get_cases/${projectId}`;
    const params: string[] = [];
    if (suiteId) params.push(`suite_id=${suiteId}`);
    if (sectionId) params.push(`section_id=${sectionId}`);
    if (limit) params.push(`limit=${limit}`);
    if (offset) params.push(`offset=${offset}`);
    if (filter) params.push(`filter=${encodeURIComponent(filter)}`);
    if (params.length > 0) endpoint += `&${params.join('&')}`;

    const result = await this.request<{ cases: TestRailCase[] }>(
      'GET',
      endpoint,
    );
    return result.cases ?? result as unknown as TestRailCase[];
  }

  async addCase(
    sectionId: number,
    payload: TestRailCasePayload,
  ): Promise<TestRailCase> {
    return this.request<TestRailCase>(
      'POST',
      `add_case/${sectionId}`,
      payload,
    );
  }

  async updateCase(
    caseId: number,
    payload: Partial<TestRailCasePayload>,
  ): Promise<TestRailCase> {
    return this.request<TestRailCase>(
      'POST',
      `update_case/${caseId}`,
      payload,
    );
  }

  async addRun(
    projectId: number,
    payload: TestRailRunPayload,
  ): Promise<TestRailRun> {
    return this.request<TestRailRun>(
      'POST',
      `add_run/${projectId}`,
      payload,
    );
  }

  async addResultForCase(
    runId: number,
    caseId: number,
    payload: TestRailResultPayload,
  ): Promise<TestRailResult> {
    return this.request<TestRailResult>(
      'POST',
      `add_result_for_case/${runId}/${caseId}`,
      payload,
    );
  }

  async getResultsForCase(
    runId: number,
    caseId: number,
    limit?: number,
  ): Promise<TestRailResult[]> {
    let endpoint = `get_results_for_case/${runId}/${caseId}`;
    if (limit) endpoint += `&limit=${limit}`;

    const result = await this.request<{ results: TestRailResult[] }>(
      'GET',
      endpoint,
    );
    return result.results ?? result as unknown as TestRailResult[];
  }
}
