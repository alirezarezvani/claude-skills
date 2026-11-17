# Google Play release rules the gate checks

Rules verified 2026-11-17. 🟢 read on the official page this session, 🟡 official but not re-read this session, 🔴 practitioner consensus.

## Target API level [1][2]

🟢 From **August 31, 2026**, new apps and app updates must target:

| Form factor | Minimum targetSdk |
|---|---|
| Phone and tablet | 36 (Android 16) |
| Wear OS, Android Automotive OS | 35 |
| Android TV, Android XR | 34 |

- 🟢 Existing apps must target **35 or higher** to stay available to new users on devices running a newer Android version than the app targets.
- 🟢 An extension to **November 1, 2026** could be requested in Play Console.
- 🟢 Permanently private apps for one organisation are exempt.
- The script's rule table starts on 2026-08-31. Before that date, or after the next annual raise (usually announced for late August), re-read [1].

## Manifest

- 🟡 Apps targeting **Android 12 (API 31)** or higher must set `android:exported` on every activity, service and receiver with an intent filter, or the app cannot be installed. [3]
- 🟡 Play does not accept APKs or bundles with `android:debuggable="true"`. [4]
- 🔴 App-wide `usesCleartextTraffic="true"` is a security review flag; scope cleartext per domain with a network security config. [5]

## Permissions that need a declaration [6]

🟡 Play's sensitive-permission policies require a Play Console declaration (sometimes with a demo video) before release for: SMS and Call Log permissions, `ACCESS_BACKGROUND_LOCATION`, `MANAGE_EXTERNAL_STORAGE`, `QUERY_ALL_PACKAGES`, `REQUEST_INSTALL_PACKAGES`, exact alarms, full-screen intents, accessibility and VPN services, photo and video permissions, and each foreground service type. The script lists them; the Console decides.

The Data safety form must describe data the app and its SDKs collect or share; a new location or contacts permission is the usual reason it goes stale. [7]

## 16 KB memory pages [8]

- 🟢 Apps targeting Android 15 (API 35) and higher must support 16 KB page sizes on 64-bit devices. **From February 1, 2027**, updates that do not cannot be released.
- 🟢 AGP **8.5.1+** and NDK **r28+** produce compatible builds by default; verify with `zipalign -c -P 16 -v 4 app.apk`. A prebuilt `.so` is compatible when every `LOAD` segment has `align 2**14`; the script reads the ELF headers of `.so` files in the project and names any below 16384.

## Sources

1. Android Developers, "Meet Google Play's target API level requirement", developer.android.com/google/play/requirements/target-sdk
2. Play Console Help, "Target API level requirements for Google Play apps", support.google.com/googleplay/android-developer/answer/11926878
3. Android Developers, "Behavior changes: apps targeting Android 12", developer.android.com/about/versions/12/behavior-changes-12
4. Android Developers, "Prepare your app for release", developer.android.com/studio/publish/preparing
5. Android Developers, "Network security configuration", developer.android.com/privacy-and-security/security-config
6. Google Play Developer Policy Center, "Permissions and APIs that Access Sensitive Information", play.google/developer-content-policy/
7. Play Console Help, "Provide information for Google Play's Data safety section", support.google.com/googleplay/android-developer/answer/10787469
8. Android Developers, "Support 16 KB page sizes", developer.android.com/guide/practices/page-sizes
