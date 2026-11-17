# Mobile release sign-off

Release: ________  Platform: iOS / Android  Owner: ________  Date: ________

## Before upload
- [ ] `ios_privacy_manifest_check.py` exit 0 or 2, every WARN read (iOS)
- [ ] Each declared reason code matches what the code does (named reviewer: ________)
- [ ] Vendored SDKs on versions that ship their own PrivacyInfo.xcprivacy
- [ ] App Store privacy label matches NSPrivacyCollectedDataTypes
- [ ] `android_release_check.py` exit 0 or 2 for the date of submission (Android)
- [ ] Play Console declarations filed for every DECLARATION_REQUIRED permission
- [ ] Data safety form updated for new permissions or SDKs
- [ ] Native libraries 16 KB aligned (`zipalign -c -P 16 -v 4 app.apk`)

## Rollout
- [ ] Baseline release and its crash/ANR counts recorded
- [ ] Gate run at each step; result pasted below
- [ ] Halt owner on call for the first 48 hours: ________

| Step | Date | Users | Crash % | ANR % | Gate | Decision by |
|---|---|---|---|---|---|---|
| | | | | | | |
