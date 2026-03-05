import type {
  BrowserStackConfig,
  BrowserStackPlan,
  BrowserStackBrowser,
  BrowserStackBuild,
  BrowserStackSession,
  BrowserStackSessionUpdate,
} from './types.js';

export class BrowserStackClient {
  private readonly baseUrl = 'https://api.browserstack.com';
  private readonly headers: Record<string, string>;

  constructor(config: BrowserStackConfig) {
    const auth = Buffer.from(`${config.username}:${config.accessKey}`).toString('base64');
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
    const url = `${this.baseUrl}${endpoint}`;
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
        `BrowserStack API error ${response.status}: ${errorText}`,
      );
    }

    return response.json() as Promise<T>;
  }

  async getPlan(): Promise<BrowserStackPlan> {
    return this.request<BrowserStackPlan>('GET', '/automate/plan.json');
  }

  async getBrowsers(): Promise<BrowserStackBrowser[]> {
    return this.request<BrowserStackBrowser[]>('GET', '/automate/browsers.json');
  }

  async getBuilds(limit?: number, status?: string): Promise<BrowserStackBuild[]> {
    let endpoint = '/automate/builds.json';
    const params: string[] = [];
    if (limit) params.push(`limit=${limit}`);
    if (status) params.push(`status=${status}`);
    if (params.length > 0) endpoint += `?${params.join('&')}`;
    return this.request<BrowserStackBuild[]>('GET', endpoint);
  }

  async getSessions(buildId: string, limit?: number): Promise<BrowserStackSession[]> {
    let endpoint = `/automate/builds/${buildId}/sessions.json`;
    if (limit) endpoint += `?limit=${limit}`;
    return this.request<BrowserStackSession[]>('GET', endpoint);
  }

  async getSession(sessionId: string): Promise<BrowserStackSession> {
    return this.request<BrowserStackSession>(
      'GET',
      `/automate/sessions/${sessionId}.json`,
    );
  }

  async updateSession(
    sessionId: string,
    update: BrowserStackSessionUpdate,
  ): Promise<BrowserStackSession> {
    return this.request<BrowserStackSession>(
      'PUT',
      `/automate/sessions/${sessionId}.json`,
      update,
    );
  }

  async getSessionLogs(sessionId: string): Promise<string> {
    const url = `${this.baseUrl}/automate/sessions/${sessionId}/logs`;
    const response = await fetch(url, { headers: this.headers });
    if (!response.ok) {
      throw new Error(`BrowserStack logs error ${response.status}`);
    }
    return response.text();
  }
}
