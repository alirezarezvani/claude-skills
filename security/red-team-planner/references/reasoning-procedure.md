# Reasoning Procedure — Detailed Steps

Execute the following 8-step procedure for every campaign planning request. Do not skip steps. Document each step's output in your response.

## Step 1 — Authorization Verification
Confirm explicit written authorization exists. Check for: sponsor name, authorized scope (IP ranges, domains, cloud accounts), engagement start/end dates, emergency stop contacts, and out-of-scope exclusions. If any element is missing, output a HALT notice and list the missing elements. Do not proceed to Step 2 without complete authorization documentation.

## Step 2 — Intelligence Collection and Threat Modeling
Profile the target organization using open-source intelligence framing. Identify industry vertical, regulatory environment, known technology stack, likely security maturity, and historical breach data if public. Map the most probable threat actor TTPs relevant to this organization's threat landscape. Reference MITRE ATT&CK groups relevant to the sector.

## Step 3 — Crown Jewels and Asset Tier Mapping
Identify and classify all known target assets into the tier classification table. For each Crown Jewel asset, document: what data or capability it contains, what an attacker would do with access, and what business impact compromise represents. This output feeds the attack objective hierarchy.

## Step 4 — Campaign Objective Hierarchy
Define primary, secondary, and tertiary objectives in priority order. Primary objectives target Crown Jewels. Secondary objectives target Tier 1 assets. Tertiary objectives use Tier 3 assets as pivots. Each objective must state: success criteria, failure criteria, and minimum access level required.

## Step 5 — Attack Path Planning
Design three to five distinct attack paths from assumed external adversary position to primary objectives. For each path, document: entry vector (MITRE Initial Access technique), prerequisites (what must be true for this path to be viable), intermediate pivot points, privilege requirements at each hop, and estimated dwell time. Flag which path has the highest probability of success given the threat model.

## Step 6 — Social Engineering and Physical Security Angles
Enumerate social engineering scenarios that support the campaign. For each scenario, document: target persona, pretext narrative, delivery mechanism (phishing, vishing, smishing, in-person), expected yield, and detection probability. If physical security testing is in scope, document facility access scenarios including tailgating, badge cloning, and dumpster diving opportunities.

## Step 7 — PTES Phase Mapping
Map the complete campaign to PTES methodology phases: Pre-engagement Interactions, Intelligence Gathering, Threat Modeling, Vulnerability Analysis, Exploitation, Post Exploitation, and Reporting. Assign responsible agents and human operators to each phase. Define go/no-go gates between phases.

## Step 8 — Rules of Engagement Enforcement Checklist
Before finalizing the campaign plan, verify every item in the RoE checklist (see MUST DO section). Output the checklist as a signed-off document. Any unchecked item blocks campaign approval.
