export interface BrowserStackConfig {
  username: string;
  accessKey: string;
}

export interface BrowserStackPlan {
  automate_plan: string;
  parallel_sessions_running: number;
  team_parallel_sessions_max_allowed: number;
  parallel_sessions_max_allowed: number;
  queued_sessions: number;
  queued_sessions_max_allowed: number;
}

export interface BrowserStackBrowser {
  os: string;
  os_version: string;
  browser: string;
  browser_version: string;
  device: string | null;
  real_mobile: boolean | null;
}

export interface BrowserStackBuild {
  automation_build: {
    name: string;
    hashed_id: string;
    duration: number;
    status: string;
    build_tag: string | null;
  };
}

export interface BrowserStackSession {
  automation_session: {
    name: string;
    duration: number;
    os: string;
    os_version: string;
    browser_version: string;
    browser: string;
    device: string | null;
    status: string;
    hashed_id: string;
    reason: string;
    build_name: string;
    project_name: string;
    logs: string;
    browser_url: string;
    public_url: string;
    video_url: string;
    browser_console_logs_url: string;
    har_logs_url: string;
  };
}

export interface BrowserStackSessionUpdate {
  name?: string;
  status?: 'passed' | 'failed';
  reason?: string;
}
