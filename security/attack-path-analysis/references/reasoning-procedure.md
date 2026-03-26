# Reasoning Procedure — Detailed Steps

Execute the following 8-step procedure for every attack path analysis request. Document each step's output before proceeding.

## Step 1 — Environment Graph Construction
Ingest available environment data: AD domain topology, BloodHound export data, Azure AD conditional access policies, AWS IAM role trust relationships, and network segmentation data. Construct a directed graph where: nodes represent assets (hosts, accounts, roles, groups, cloud resources) and edges represent attack vectors (credential reuse, group membership, IAM role assumption, trust relationship exploitation). Label each edge with its path category and prerequisite conditions.

## Step 2 — Entry Point Enumeration
Define all plausible attacker entry points based on the engagement scope and threat model. Entry points include: phishing-compromised user accounts (Tier 3 access), VPN credential theft, publicly exposed services, supply chain compromise positions, and any assumed breach starting positions defined by the campaign. Each entry point becomes a root node in the path analysis.

## Step 3 — Crown Jewel Node Identification
Identify all Crown Jewel nodes in the graph: domain controllers, certificate authority servers, HSMs, source code repositories, production databases with PII or financial data, and any asset explicitly designated as Crown Jewel by the campaign plan. These are the terminal target nodes for path analysis.

## Step 4 — Shortest Path Enumeration
From each entry point, enumerate all paths to each Crown Jewel node using Dijkstra-equivalent path traversal weighted by prerequisite cost (lower prerequisite cost = shorter effective path). Identify: the single shortest path (fewest hops), the highest-scored path (best composite likelihood-impact-stealth score), and all paths that pass through fewer than five nodes.

## Step 5 — Path Scoring and Ranking
Apply the path scoring matrix to each enumerated path. Calculate composite scores. Rank all paths from highest to lowest composite score. Flag any path with a composite score above 7.0 as a critical path requiring immediate hardening attention regardless of whether it was exploited during the engagement.

## Step 6 — Choke Point Identification
Analyze the path graph to identify nodes that appear in the largest number of critical paths. For each candidate choke point, calculate: the number of critical paths it appears in, what hardening action would remove it from the graph (disable account, require MFA, remove group membership, revoke IAM role), and the remediation complexity. Score each choke point and classify by priority.

## Step 7 — Cloud and Hybrid Path Analysis
Extend the graph to cloud environments. For Azure AD / Entra ID: analyze conditional access policy gaps, PIM role assignments, service principal permissions, and Managed Identity abuse paths. For AWS IAM: analyze cross-account trust policies, role chaining (assume-role chains longer than two hops), resource-based policy misconfigurations, and privilege escalation via policy attachment. Flag any path that crosses the on-premises to cloud boundary as a hybrid path — these are highest-priority findings.

## Step 8 — Hardening Recommendation Generation
For each choke point and critical path, produce specific, actionable hardening recommendations. Each recommendation must include: the specific configuration change required, the system or account it applies to, the path categories it blocks, and the estimated implementation effort (hours). Rank recommendations by choke point score — highest-impact remediations first.
