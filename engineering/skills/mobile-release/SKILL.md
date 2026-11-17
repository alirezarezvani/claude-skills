---
name: mobile-release
description: "Get an iOS or Android app release through App Store and Google Play review, then roll it out safely. Use before submitting or uploading a build, when App Store Connect or Play Console rejects one (privacy manifest, required reason API, missing purpose string, target API level, exported components, permission declarations) or when deciding whether to widen, pause or halt a staged or phased rollout from crash and ANR numbers."
argument-hint: "[ios project dir | android project dir | rollout.csv]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Three deterministic stdlib scripts (iOS privacy manifest and purpose-string check, Android Play release check, staged-rollout gate) with blocking exit codes; rules cited to Apple's Bundle Resources and App Store Connect documentation, Apple Upcoming Requirements, developer.android.com target-SDK and 16 KB page-size pages and the Android Developers Blog on Play core vitals"
  distinct_from: "app-store-optimization (store listing, keywords, conversion; this gates the binary and the rollout); ship-gate (pre-production audit for web services); release-management advice in senior-devops (CI/CD, not store review)"
---

# Mobile Release

> **Portability:** 3 stdlib Python scripts. They read project files only. No network, no store API calls.
> **Rules verified 2026-11-17.** Store rules move every year; each script prints the date its table was checked.

Most store rejections and bad rollouts come from a short list of mechanical
misses: an API Apple requires a reason for, a purpose string that was never
added, a targetSdk one level behind, a receiver without `android:exported`,
a crash spike that was widened to 50% because nobody compared it with the last
release. This skill checks each one before it costs a review cycle.

## Workflow

```bash
# 1 - iOS: required-reason APIs vs PrivacyInfo.xcprivacy, purpose strings, SDK manifests
python scripts/ios_privacy_manifest_check.py --project ios/
# 2 - Android: Play target API level, exported components, declaration permissions, 16 KB pages
python scripts/android_release_check.py --project android/ --form-factor phone
# 3 - During rollout: compare the new release with the last one, then widen, hold or halt
python scripts/rollout_gate.py --input rollout.csv
```

**Step 1** finds code that uses a required-reason API category (file
timestamps, system boot time, disk space, active keyboards, UserDefaults) and
checks the app manifest declares it with a reason Apple lists for that
category. It blocks invalid and SDK-only reasons, a framework used without its
`NS...UsageDescription` (Info.plist or `INFOPLIST_KEY_` build setting), and
warns when a vendored SDK ships no manifest of its own. Pick the reason that
is **true**; an upload that passes is not proof the reason is right.

**Step 2** reads targetSdk from Gradle (including Capacitor `variables.gradle`
and version catalogs) and applies Play's dated rule for the form factor. It
blocks debuggable builds and intent-filter components with no
`android:exported`, and lists permissions that need a Play Console declaration
before release (background location, SMS, all-files access, exact alarms,
foreground service types).

**Step 3** needs counts, not percentages: users and crashed users for the
baseline and the new release. It halts on Play's bad-behavior thresholds or a
statistically significant regression, and holds when the regression is not yet
significant or the release has too few users.

## Hard rules

- **A BLOCKER means do not submit.** Fix it, re-run, then upload.
- **Never declare a reason code to make the check pass.** Ask what the code does with the API, then pick the reason.
- **The app's manifest cannot cover an SDK.** Update the SDK to a version that ships its own manifest.
- **Never widen a rollout on a percentage alone.** Feed the gate counts for both releases.
- **iOS cannot roll back.** A paused phased release is still downloadable by hand; plan the fix or pull the build.
- **Re-check dates.** If today is past a date in a script's rule table, confirm against the official page in the references.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/ios_privacy_manifest_check.py` | Required-reason APIs, reason codes, purpose strings, SDK manifests, tracking keys | 0 · 2 warnings · 3 bad input · 4 blocked |
| `scripts/android_release_check.py` | Target API level by date and form factor, exported, debuggable, declarations, 16 KB | 0 · 2 warnings · 3 bad input · 4 blocked |
| `scripts/rollout_gate.py` | PROCEED / HOLD / HALT from crash and ANR counts vs baseline | 0 proceed · 2 hold · 3 bad input · 4 halt |

All support `--help`, `--sample` and `--output json`.

## References and assets

- [`references/ios_submission_rules.md`](references/ios_submission_rules.md): privacy manifests, reason codes, purpose strings, SDK and Xcode minimums (7 sources)
- [`references/play_release_rules.md`](references/play_release_rules.md): target API levels, exported, declarations, Data safety, 16 KB pages (7 sources)
- [`references/staged_rollout_gates.md`](references/staged_rollout_gates.md): phased vs staged rollout, vitals thresholds, the regression test (6 sources)
- [`assets/rollout.example.csv`](assets/rollout.example.csv): input format for the gate
- [`assets/release_checklist.md`](assets/release_checklist.md): submission and rollout sign-off
