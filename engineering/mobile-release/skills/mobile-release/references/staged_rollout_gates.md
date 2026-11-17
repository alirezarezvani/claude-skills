# Staged and phased rollout gates

Verified 2026-11-17. 🟢 read on the official page this session, 🟡 official not re-read, 🔴 practice.

## The two mechanisms differ

| | iOS phased release [1] | Android staged rollout [2] |
|---|---|---|
| Percentages | 🟢 Fixed: 1, 2, 5, 10, 20, 50, 100% over 7 days | Set by you at each step |
| Stop | 🟢 Pause up to 30 days (any number of times), or release to all | 🟡 Halt; resume or replace with a new version code |
| Who still gets it | 🟢 Anyone can download it manually while paused | 🟡 Users already updated keep it |
| Applies to | Automatic updates only | New and updating users in the chosen fraction |

Neither store rolls a user back. A bad iOS build stays in the hands of everyone who downloaded it, so the gate's job is to stop early.

## Play core vitals [3]

🟢 Bad-behavior thresholds: user-perceived crash rate **1.09%**, user-perceived ANR rate **0.47%** across all devices, and **8%** on any single phone model. Above them an app can lose visibility, and a per-device breach can bring a store-listing warning on that model. The gate halts at these values regardless of baseline.

Play computes these as daily users who experienced the event over daily active users. Feeding the gate per-release user counts from Play Console Android vitals (or your crash reporter, same definition for both releases) keeps the comparison like for like.

## The regression test

A rate on 800 users means little: 2 crashes is 0.25%, 1 crash is 0.125%. The gate therefore
1. holds below `--min-users` (default 1000),
2. compares the new release with the baseline using a one-sided two-proportion z-test [4],
3. halts only when the relative worsening is above `--max-regression` (default 25%) **and** p < `--alpha` (default 0.05); holds when it is above but not significant.

Defaults are judgement calls (🔴), state them when you report a decision. Repeated looks at a growing sample inflate false alarms [5]; that is acceptable here because a false HOLD costs a day and a missed HALT costs the user base. Google's SRE canary guidance makes the same trade: compare canary and control on the same metric, over a population large enough to detect the difference you care about [6].

## Sources

1. App Store Connect Help, "Release a version update in phases", developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases
2. Play Console Help, "Release app updates with staged rollouts", support.google.com/googleplay/android-developer/answer/6346149
3. Android Developers Blog, "Raising the bar on technical quality on Google Play" (Oct 2022), android-developers.googleblog.com/2022/10/raising-bar-on-technical-quality-on-google-play.html; Android vitals overview, developer.android.com/topic/performance/vitals
4. NIST/SEMATECH e-Handbook of Statistical Methods, 7.3.3 "How can we determine whether two processes produce the same proportion of defectives?"
5. Armitage, McPherson & Rowe (1969), "Repeated significance tests on accumulating data", JRSS A 132(2)
6. Google, The Site Reliability Workbook, ch. 16 "Canarying Releases", sre.google/workbook/canarying-releases/
