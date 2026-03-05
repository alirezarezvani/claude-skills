export interface TestRailConfig {
  url: string;
  user: string;
  apiKey: string;
}

export interface TestRailProject {
  id: number;
  name: string;
  announcement: string;
  is_completed: boolean;
  suite_mode: number;
  url: string;
}

export interface TestRailSuite {
  id: number;
  name: string;
  description: string | null;
  project_id: number;
  url: string;
}

export interface TestRailSection {
  id: number;
  suite_id: number;
  name: string;
  description: string | null;
  parent_id: number | null;
  depth: number;
}

export interface TestRailCaseStep {
  content: string;
  expected: string;
}

export interface TestRailCase {
  id: number;
  title: string;
  section_id: number;
  template_id: number;
  type_id: number;
  priority_id: number;
  estimate: string | null;
  refs: string | null;
  custom_preconds: string | null;
  custom_steps_separated: TestRailCaseStep[] | null;
  custom_steps: string | null;
  custom_expected: string | null;
}

export interface TestRailRun {
  id: number;
  suite_id: number;
  name: string;
  description: string | null;
  assignedto_id: number | null;
  include_all: boolean;
  is_completed: boolean;
  passed_count: number;
  failed_count: number;
  untested_count: number;
  url: string;
}

export interface TestRailResult {
  id: number;
  test_id: number;
  status_id: number;
  comment: string | null;
  created_on: number;
  elapsed: string | null;
  defects: string | null;
}

export interface TestRailResultPayload {
  status_id: number;
  comment?: string;
  elapsed?: string;
  defects?: string;
}

export interface TestRailRunPayload {
  suite_id?: number;
  name: string;
  description?: string;
  assignedto_id?: number;
  include_all?: boolean;
  case_ids?: number[];
  refs?: string;
}

export interface TestRailCasePayload {
  title: string;
  template_id?: number;
  type_id?: number;
  priority_id?: number;
  estimate?: string;
  refs?: string;
  custom_preconds?: string;
  custom_steps_separated?: TestRailCaseStep[];
  custom_steps?: string;
  custom_expected?: string;
}
