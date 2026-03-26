# Behavioral Baseline Methodology

## Baseline Dimensions by Entity Type

### User Accounts

| Dimension | Baseline Metric | Unit |
|---|---|---|
| Login hours | Mean and standard deviation of login timestamps | Hour-of-day distribution |
| Login locations | Set of observed source IPs, countries, ASNs | Location set |
| Volume of files accessed | Daily file access count (mean, p95) | Files/day |
| Volume of data egressed | Daily bytes uploaded/emailed externally | Bytes/day |
| Applications accessed | Set of applications used weekly | Application set |
| Privileged command usage | Count of sudo / admin actions per day | Actions/day |
| Devices used | Set of device fingerprints (MAC, hostname) | Device set |

### Service Accounts

| Dimension | Baseline Metric | Unit |
|---|---|---|
| Caller hosts | Set of hosts that invoke the service account | Host set |
| API call patterns | Ordered sequence of API actions called | Sequence |
| Call volume | API calls per hour (mean, p95) | Calls/hour |
| Time of operation | Expected operation windows | Time range |

### Workstations and Servers

| Dimension | Baseline Metric | Unit |
|---|---|---|
| Outbound connection destinations | Set of destination IPs and domains | Destination set |
| Process execution patterns | Set of processes and their parent relationships | Process tree |
| Authentication sources | Set of accounts that log into this host | Account set |
| Network throughput | Bytes in / bytes out per hour (mean, p95) | Bytes/hour |

Baseline cold-start handling: Entities with fewer than 30 days of data are flagged as "baseline insufficient." Risk scores for these entities carry a confidence penalty of 0.5 and require analyst review before automated action.

---

## Anomaly Category Examples

### Category 1: Time Anomaly
Example: A finance analyst whose logins have occurred between 08:00 and 18:30 for 90 days logs in at 03:17 from the same IP. Time anomaly score = high.

### Category 2: Volume Anomaly
Example: A user's baseline daily egress is 12 MB. Today they have uploaded 4.7 GB to a cloud storage service. Volume anomaly = critical.

### Category 3: Peer Group Anomaly
Example: All other engineers in the platform team access an average of 200 code repos per month. One engineer accessed 1,400 repos this month, including repos outside their team scope. Peer group anomaly = high.

---

## Insider Threat Composite Indicators

**Pattern A: Disgruntled Employee + Data Staging**
Trigger conditions (ALL required):
- HR flag in system: performance improvement plan, disciplinary action, or resignation notice within last 90 days.
- Bulk download event with data_sensitivity_factor >= 1.5.
- Any after-hours access in the past 7 days.

**Pattern B: Pre-Departure Exfiltration**
Trigger conditions (ALL required):
- Account is flagged as termination-pending in HR system.
- Bulk download or USB activity.
- Access to systems outside normal role scope.

**Pattern C: Privileged Account Abuse**
Trigger conditions (ANY TWO required):
- Admin account used during non-business hours.
- Admin account used from an IP not in the approved admin workstation list.
- Admin account used to access data unrelated to current IT tasks.
- Audit log clearing or service account password change.

---

## Account Takeover Indicators

**ATO Pattern 1: Credential Change + Immediate Bulk Access**
- Password or MFA device changed.
- Within 60 minutes: bulk file access or data egress volume > 10× baseline.
- Source IP not in user's historical IP set.

**ATO Pattern 2: Geographic Impossibility**
- Successful login from Location A at T=0.
- Successful login from Location B at T=N where travel between A and B in N minutes is physically impossible.
- This is also called an "impossible travel" indicator.

**ATO Pattern 3: Session Behavior Divergence**
- Session typing cadence, mouse movement, or click patterns deviate significantly from the user's historical session fingerprint (requires endpoint behavioral sensor).
- All actions in session are oriented toward data access and egress — no navigation noise.
