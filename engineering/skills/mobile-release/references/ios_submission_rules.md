# iOS submission rules the gate checks

Rules verified 2026-11-17 against the Apple pages below. Confidence: 🟢 read on the official page this session, 🟡 official but not re-read this session, 🔴 practitioner consensus.

## Required-reason APIs and privacy manifests

- 🟢 Since **May 1, 2024**, App Store Connect does not accept apps that use a required-reason API without describing the reason in the privacy manifest. [1]
- 🟢 Each executable or dynamic library that uses one needs its own manifest in its bundle; **an SDK cannot rely on the app's manifest, and the app cannot cover an SDK.** [1]
- 🟢 The declared reasons must be accurate; the data may be used only for the declared reasons and never for tracking. [1]

| Category | APIs (examples) | Reasons | SDK-only |
|---|---|---|---|
| FileTimestamp | `creationDate`, `modificationDate`, `fileModificationDate`, `contentModificationDateKey`, `creationDateKey`, `stat`, `fstat`, `lstat`, `getattrlist*` | DDA9.1 display to user · C617.1 own container · 3B52.1 user-granted files | 0A2A.1 |
| SystemBootTime | `systemUptime`, `mach_absolute_time()` | 35F9.1 elapsed time · 8FFB.1 absolute event timestamps · 3D61.1 user bug report | - |
| DiskSpace | `volumeAvailableCapacityKey` and variants, `volumeTotalCapacityKey`, `systemFreeSize`, `systemSize`, `statfs`, `statvfs` | 85F4.1 display · E174.1 check before writing · 7D9E.1 user bug report · B728.1 health research | - |
| ActiveKeyboards | `activeInputModes` | 3EC4.1 keyboard app · 54BD.1 adapt text-field UI | - |
| UserDefaults | `UserDefaults` | CA92.1 app only · 1C8F.1 App Group · AC6B.1 MDM managed config | C56D.1 |

Source: Apple's `NSPrivacyAccessedAPIType` page [2]. Most reasons forbid sending the derived data off-device; read the full text before choosing.

**Common misreadings the script targets**
- Declaring `E174.1` (a DiskSpace reason) under FileTimestamp: the code is valid only in its own category.
- Copying an SDK's `C56D.1` or `0A2A.1` into the app manifest.
- `@AppStorage` is UserDefaults underneath (🔴 widely reported; the script treats it as usage).
- `PHAsset.creationDate` is not a file timestamp API; the script only matches FileManager/URL resource keys and the C calls.

## Tracking keys

- 🟡 `NSPrivacyTracking` says whether the app or SDK tracks as defined by App Tracking Transparency; `NSPrivacyTrackingDomains` lists the domains it contacts for tracking. Domains with tracking false is a contradiction the script flags. [3]
- 🟡 `NSPrivacyCollectedDataTypes` should agree with the App Store privacy "nutrition label". [3]

## Purpose strings

- 🟡 An app that requests a protected resource without the matching `NS...UsageDescription` key is terminated by the system at the request, and App Review guideline 5.1.1 requires a clear purpose string. [4][5]
- 🟢 Xcode projects that generate Info.plist store these as `INFOPLIST_KEY_<key>` build settings in `project.pbxproj`; the script reads both.

## Platform minimums (Apple Upcoming Requirements) [6]

- 🟢 Since **April 28, 2026**: uploads must be built with **Xcode 26 or later** using an iOS/iPadOS/tvOS/visionOS/watchOS **26 SDK**.
- 🟢 Since **September 9, 2026**: iOS and iPadOS uploads must target **iOS 13 or later**.
- 🟢 Age-rating questions had to be answered by **January 31, 2026** to avoid interruption when submitting updates.
- 🟢 Since **February 17, 2025**: apps without verified DSA trader status are removed from the EU storefronts.

## Sources

1. Apple, "Describing use of required reason API", developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api
2. Apple, "NSPrivacyAccessedAPIType", developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacyaccessedapitypes/nsprivacyaccessedapitype
3. Apple, "Privacy manifest files", developer.apple.com/documentation/bundleresources/privacy-manifest-files
4. Apple, "Requesting access to protected resources", developer.apple.com/documentation/uikit/requesting-access-to-protected-resources
5. Apple, App Review Guidelines 5.1.1 Data Collection and Storage, developer.apple.com/app-store/review/guidelines/
6. Apple, "Upcoming Requirements", developer.apple.com/news/upcoming-requirements/
7. Apple WWDC23 session 10060, "Get started with privacy manifests"
