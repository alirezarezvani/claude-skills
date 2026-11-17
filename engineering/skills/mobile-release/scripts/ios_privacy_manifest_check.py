#!/usr/bin/env python3
"""Check an iOS project's privacy manifest and purpose strings before upload.

App Store Connect has refused uploads since May 1, 2024 when code uses a
"required reason" API that the privacy manifest (PrivacyInfo.xcprivacy) does
not declare with an approved reason. A missing purpose string (Info.plist
NS...UsageDescription) crashes the app the first time it asks for that
permission and is a common App Review rejection. This script scans source code
for both and compares it with what the project declares.

Findings
  UNDECLARED_CATEGORY  app code uses a required-reason API category the app
                       manifest does not list                               BLOCKER
  NO_APP_MANIFEST      required-reason API used and no app PrivacyInfo.xcprivacy BLOCKER
  INVALID_REASON       reason code is not one Apple lists for that category  BLOCKER
  SDK_ONLY_REASON      reason reserved for third-party SDKs (0A2A.1, C56D.1)
                       declared in the app's own manifest                   BLOCKER
  UNKNOWN_CATEGORY     NSPrivacyAccessedAPIType value Apple does not define  BLOCKER
  EMPTY_REASONS        category declared with no reasons                     BLOCKER
  MISSING_PURPOSE      framework that needs a purpose string is used and no
                       NS...UsageDescription is set (Info.plist or
                       INFOPLIST_KEY_ build setting)                        BLOCKER
  SDK_WITHOUT_MANIFEST third-party SDK folder uses required-reason API and
                       ships no PrivacyInfo.xcprivacy of its own            WARN
  TRACKING_NO_DOMAINS  NSPrivacyTracking true but no NSPrivacyTrackingDomains WARN
  DOMAINS_NOT_TRACKING tracking domains listed while NSPrivacyTracking false  WARN
  NO_COLLECTED_TYPES   app manifest has no NSPrivacyCollectedDataTypes key   WARN
  DECLARED_NOT_SEEN    category declared but not found in source (may be in a
                       binary dependency; keep it only if true)             INFO

Detection is lexical (symbol names in .swift/.m/.mm/.h/.c/.cpp), so it can
over-report (a variable named systemUptime) and cannot see inside compiled
binaries. Confirm each BLOCKER against the code before declaring a reason:
the declared reason must be true, not merely accepted.

Exit codes: 0 clean, 2 warnings only, 3 bad input, 4 blocked.
Rules verified against Apple's documentation on 2026-11-17.
Deterministic, stdlib only, no network.
"""
import argparse
import json
import os
import plistlib
import re
import sys

RULES_VERIFIED = "2026-11-17"
EXIT = {"CLEAN": 0, "WARNINGS": 2, "BAD_INPUT": 3, "BLOCKED": 4}
SOURCE_EXT = {".swift", ".m", ".mm", ".h", ".c", ".cc", ".cpp"}
THIRD_PARTY_DIRS = {"Pods", "Carthage", "SourcePackages", "node_modules", "vendor", ".build", "checkouts"}
SKIP_DIRS = {".git", "DerivedData", "build", "Build"}

# Category -> {reason: (sdk_only, summary)}; from Apple's NSPrivacyAccessedAPIType docs.
CATEGORIES = {
    "NSPrivacyAccessedAPICategoryFileTimestamp": {
        "DDA9.1": (False, "display file timestamps to the user; not sent off-device"),
        "C617.1": (False, "metadata of files in the app, app group or CloudKit container"),
        "3B52.1": (False, "metadata of files the user granted access to (document picker)"),
        "0A2A.1": (True, "third-party SDK wrapper called by the app"),
    },
    "NSPrivacyAccessedAPICategorySystemBootTime": {
        "35F9.1": (False, "measure elapsed time between in-app events / timers"),
        "8FFB.1": (False, "compute absolute timestamps for in-app events"),
        "3D61.1": (False, "optional user-submitted bug report"),
    },
    "NSPrivacyAccessedAPICategoryDiskSpace": {
        "85F4.1": (False, "display disk space to the user"),
        "E174.1": (False, "check space before writing files / clean up when low"),
        "7D9E.1": (False, "optional user-submitted bug report"),
        "B728.1": (False, "health research app warning about low space"),
    },
    "NSPrivacyAccessedAPICategoryActiveKeyboards": {
        "3EC4.1": (False, "custom keyboard app"),
        "54BD.1": (False, "adapt UI of text fields to the active keyboard"),
    },
    "NSPrivacyAccessedAPICategoryUserDefaults": {
        "CA92.1": (False, "read/write data only this app can access"),
        "1C8F.1": (False, "read/write data shared within the same App Group"),
        "C56D.1": (True, "third-party SDK wrapper called by the app"),
        "AC6B.1": (False, "managed app configuration / feedback keys set by MDM"),
    },
}

SYMBOLS = {
    "NSPrivacyAccessedAPICategoryFileTimestamp": [
        r"\bNSFileCreationDate\b", r"\bNSFileModificationDate\b", r"\bfileModificationDate\b",
        r"\bcontentModificationDateKey\b", r"\bcreationDateKey\b",
        r"\bNSURLContentModificationDateKey\b", r"\bNSURLCreationDateKey\b",
        r"FileAttributeKey\.(?:creationDate|modificationDate)\b",
        r"\[\s*\.(?:creationDate|modificationDate)\s*\]",
        r"\b(?:stat|fstat|fstatat|lstat|getattrlist|getattrlistbulk|fgetattrlist|getattrlistat)\s*\(",
    ],
    "NSPrivacyAccessedAPICategorySystemBootTime": [
        r"\bsystemUptime\b", r"\bmach_absolute_time\s*\(",
    ],
    "NSPrivacyAccessedAPICategoryDiskSpace": [
        r"\bvolumeAvailableCapacity(?:ForImportantUsage|ForOpportunisticUsage)?Key\b",
        r"\bvolumeTotalCapacityKey\b", r"\bNSURLVolume(?:Available|Total)Capacity\w*Key\b",
        r"\bsystemFreeSize\b", r"\bsystemSize\b", r"\bNSFileSystem(?:Free)?Size\b",
        r"\b(?:statfs|statvfs|fstatfs|fstatvfs)\s*\(",
    ],
    "NSPrivacyAccessedAPICategoryActiveKeyboards": [r"\bactiveInputModes\b"],
    "NSPrivacyAccessedAPICategoryUserDefaults": [
        r"\bUserDefaults\b", r"\bNSUserDefaults\b", r"@AppStorage\b",
    ],
}
SYMBOL_RE = {c: re.compile("|".join(p)) for c, p in SYMBOLS.items()}

# Framework use -> purpose-string keys (any one satisfies).
PURPOSE = [
    (r"\bAVCaptureDevice\b|\bUIImagePickerController\b.*\.camera|\bAVCaptureSession\b", ["NSCameraUsageDescription"]),
    (r"\bAVAudioRecorder\b|\brequestRecordPermission\b|\bAVAudioApplication\.requestRecordPermission", ["NSMicrophoneUsageDescription"]),
    (r"\bCLLocationManager\b", ["NSLocationWhenInUseUsageDescription", "NSLocationAlwaysAndWhenInUseUsageDescription"]),
    (r"\bPHPhotoLibrary\b|\bPHAsset\.fetch", ["NSPhotoLibraryUsageDescription", "NSPhotoLibraryAddUsageDescription"]),
    (r"\bCNContactStore\b", ["NSContactsUsageDescription"]),
    (r"\bEKEventStore\b", ["NSCalendarsFullAccessUsageDescription", "NSCalendarsWriteOnlyAccessUsageDescription", "NSCalendarsUsageDescription", "NSRemindersFullAccessUsageDescription"]),
    (r"\bATTrackingManager\b", ["NSUserTrackingUsageDescription"]),
    (r"\bHKHealthStore\b", ["NSHealthShareUsageDescription", "NSHealthUpdateUsageDescription"]),
    (r"\bCBCentralManager\b|\bCBPeripheralManager\b", ["NSBluetoothAlwaysUsageDescription"]),
    (r"\bLAContext\b", ["NSFaceIDUsageDescription"]),
    (r"\bSFSpeechRecognizer\b", ["NSSpeechRecognitionUsageDescription"]),
    (r"\bCMMotionActivityManager\b|\bCMPedometer\b", ["NSMotionUsageDescription"]),
    (r"\bNFCNDEFReaderSession\b|\bNFCTagReaderSession\b", ["NFCReaderUsageDescription"]),
]
PURPOSE_RE = [(re.compile(p), keys) for p, keys in PURPOSE]

SAMPLE_FILES = {
    "App/Sources/Cache.swift": (
        "import Foundation\n"
        "let defaults = UserDefaults.standard\n"
        "let attrs = try FileManager.default.attributesOfItem(atPath: p)\n"
        "let made = attrs[.creationDate] as? Date\n"
        "let up = ProcessInfo.processInfo.systemUptime\n"
    ),
    "App/Sources/Scanner.swift": "import AVFoundation\nlet device = AVCaptureDevice.default(for: .video)\n",
    "App/Info.plist": None,
    "App/PrivacyInfo.xcprivacy": None,
    "Pods/FastAnalytics/Disk.m": "NSDictionary *a = [fm attributesOfFileSystemForPath:p error:nil]; id f = a[NSFileSystemFreeSize];\n",
}
SAMPLE_MANIFEST = {
    "NSPrivacyTracking": False,
    "NSPrivacyTrackingDomains": ["metrics.example-ads.com"],
    "NSPrivacyAccessedAPITypes": [
        {"NSPrivacyAccessedAPIType": "NSPrivacyAccessedAPICategoryUserDefaults",
         "NSPrivacyAccessedAPITypeReasons": ["CA92.1", "C56D.1"]},
        {"NSPrivacyAccessedAPIType": "NSPrivacyAccessedAPICategoryFileTimestamp",
         "NSPrivacyAccessedAPITypeReasons": ["E174.1"]},
    ],
}
SAMPLE_INFO = {"CFBundleIdentifier": "com.example.app"}


def write_sample(root):
    for rel, text in SAMPLE_FILES.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if rel.endswith(".xcprivacy"):
            with open(path, "wb") as fh:
                plistlib.dump(SAMPLE_MANIFEST, fh)
        elif rel.endswith("Info.plist"):
            with open(path, "wb") as fh:
                plistlib.dump(SAMPLE_INFO, fh)
        else:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)


def strip_comments(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"//[^\n]*", "", text)


def third_party_root(rel):
    """'Pods/Foo/x.m' -> 'Pods/Foo'; None for the app's own files."""
    dirs = rel.split(os.sep)[:-1]
    for i, part in enumerate(dirs):
        if part in THIRD_PARTY_DIRS:
            return os.sep.join(dirs[: i + 2])
    return None


def scan(root):
    usage = {}          # category -> list of (file, line)
    sdk_usage = {}      # sdk root -> set(categories)
    purpose_needed = {}  # key tuple -> (file, line)
    manifests, infoplists, pbx = [], [], []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.endswith(".xcassets")]
        for name in filenames:
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root)
            if name == "PrivacyInfo.xcprivacy":
                manifests.append(rel)
                continue
            if name == "Info.plist":
                infoplists.append(rel)
                continue
            if name == "project.pbxproj":
                pbx.append(rel)
                continue
            if os.path.splitext(name)[1] not in SOURCE_EXT:
                continue
            try:
                with open(path, encoding="utf-8", errors="replace") as fh:
                    text = strip_comments(fh.read())
            except OSError:
                continue
            sdk = third_party_root(rel)
            for lineno, line in enumerate(text.splitlines(), 1):
                for cat, rx in SYMBOL_RE.items():
                    if rx.search(line):
                        if sdk:
                            sdk_usage.setdefault(sdk, set()).add(cat)
                        else:
                            usage.setdefault(cat, []).append((rel, lineno))
                if sdk:
                    continue
                for rx, keys in PURPOSE_RE:
                    if rx.search(line):
                        purpose_needed.setdefault(tuple(keys), (rel, lineno))
    return usage, sdk_usage, purpose_needed, manifests, infoplists, pbx


def load_plist(path):
    with open(path, "rb") as fh:
        return plistlib.load(fh)


def check(root, app_manifest=None):
    findings = []

    def add(sev, code, msg, where=None):
        findings.append({"severity": sev, "code": code, "message": msg, "where": where})

    usage, sdk_usage, purpose_needed, manifests, infoplists, pbx = scan(root)
    app_manifests = [m for m in manifests if not third_party_root(m)]
    if app_manifest:
        app_manifests = [os.path.relpath(os.path.abspath(app_manifest), root)]
    declared = {}
    manifest_data = None
    if app_manifests:
        mpath = os.path.join(root, app_manifests[0])
        try:
            manifest_data = load_plist(mpath)
        except Exception as exc:  # plistlib raises several types
            raise ValueError(f"cannot parse {app_manifests[0]}: {exc}")
        if len(app_manifests) > 1 and not app_manifest:
            add("INFO", "MULTIPLE_APP_MANIFESTS", f"{len(app_manifests)} app-side manifests; checked {app_manifests[0]} (pass --manifest to choose)")
        for entry in manifest_data.get("NSPrivacyAccessedAPITypes", []) or []:
            cat = entry.get("NSPrivacyAccessedAPIType", "")
            reasons = entry.get("NSPrivacyAccessedAPITypeReasons", []) or []
            if cat not in CATEGORIES:
                add("BLOCKER", "UNKNOWN_CATEGORY", f"'{cat}' is not an Apple required-reason category", app_manifests[0])
                continue
            declared[cat] = reasons
            if not reasons:
                add("BLOCKER", "EMPTY_REASONS", f"{cat} has no reasons", app_manifests[0])
            for r in reasons:
                if r not in CATEGORIES[cat]:
                    add("BLOCKER", "INVALID_REASON", f"{r} is not a valid reason for {cat} (valid: {', '.join(CATEGORIES[cat])})", app_manifests[0])
                elif CATEGORIES[cat][r][0]:
                    add("BLOCKER", "SDK_ONLY_REASON", f"{r} under {cat} may only be declared by a third-party SDK, not by the app", app_manifests[0])
        tracking = manifest_data.get("NSPrivacyTracking")
        domains = manifest_data.get("NSPrivacyTrackingDomains") or []
        if tracking is True and not domains:
            add("WARN", "TRACKING_NO_DOMAINS", "NSPrivacyTracking is true but NSPrivacyTrackingDomains is empty", app_manifests[0])
        if tracking is not True and domains:
            add("WARN", "DOMAINS_NOT_TRACKING", f"{len(domains)} tracking domain(s) listed while NSPrivacyTracking is not true; one of the two is wrong", app_manifests[0])
        if "NSPrivacyCollectedDataTypes" not in manifest_data:
            add("WARN", "NO_COLLECTED_TYPES", "no NSPrivacyCollectedDataTypes; it should match the App Store privacy label", app_manifests[0])

    for cat, hits in sorted(usage.items()):
        f, ln = hits[0]
        where = f"{f}:{ln}" + (f" (+{len(hits) - 1} more)" if len(hits) > 1 else "")
        if manifest_data is None:
            continue
        if cat not in declared:
            add("BLOCKER", "UNDECLARED_CATEGORY", f"{cat} used in app code but not declared; pick the reason that is true: " + "; ".join(f"{r} {s}" for r, (sdk, s) in CATEGORIES[cat].items() if not sdk), where)
    if usage and manifest_data is None:
        cats = ", ".join(sorted(usage))
        add("BLOCKER", "NO_APP_MANIFEST", f"required-reason API used ({cats}) and no app PrivacyInfo.xcprivacy found")
    for cat in sorted(set(declared) - set(usage)):
        add("INFO", "DECLARED_NOT_SEEN", f"{cat} declared but not found in source; keep it only if a dependency compiled into the app uses it", app_manifests[0] if app_manifests else None)

    sdk_manifest_roots = {third_party_root(m) for m in manifests if third_party_root(m)}
    for sdk, cats in sorted(sdk_usage.items()):
        has = sdk in sdk_manifest_roots
        if not has:
            add("WARN", "SDK_WITHOUT_MANIFEST", f"{sdk} uses {', '.join(sorted(c.replace('NSPrivacyAccessedAPICategory', '') for c in cats))} and ships no PrivacyInfo.xcprivacy; update the SDK (the app's manifest cannot cover it)", sdk)

    set_keys = set()
    for ip in infoplists:
        if third_party_root(ip):
            continue
        try:
            set_keys |= {k for k, v in load_plist(os.path.join(root, ip)).items() if v}
        except Exception:
            add("WARN", "INFO_PLIST_UNREADABLE", "could not parse", ip)
    for p in pbx:
        if third_party_root(p):
            continue
        with open(os.path.join(root, p), encoding="utf-8", errors="replace") as fh:
            for m in re.finditer(r"INFOPLIST_KEY_(\w+)\s*=\s*\"?([^\";]*)", fh.read()):
                if m.group(2).strip():
                    set_keys.add(m.group(1))
    for keys, (f, ln) in sorted(purpose_needed.items()):
        if not set_keys & set(keys):
            add("BLOCKER", "MISSING_PURPOSE", f"needs {' or '.join(keys)} (Info.plist or INFOPLIST_KEY_ build setting); without it the permission request crashes", f"{f}:{ln}")

    blocked = any(x["severity"] == "BLOCKER" for x in findings)
    warned = any(x["severity"] == "WARN" for x in findings)
    verdict = "BLOCKED" if blocked else ("WARNINGS" if warned else "CLEAN")
    return {
        "verdict": verdict,
        "rules_verified": RULES_VERIFIED,
        "app_manifest": app_manifests[0] if app_manifests else None,
        "categories_used": {c.replace("NSPrivacyAccessedAPICategory", ""): len(h) for c, h in usage.items()},
        "categories_declared": {c.replace("NSPrivacyAccessedAPICategory", ""): r for c, r in declared.items()},
        "findings": findings,
    }


def render(res):
    out = [f"iOS privacy manifest check: {res['verdict']}  (rules verified {res['rules_verified']})",
           f"App manifest: {res['app_manifest'] or 'none found'}",
           f"Used in app code: {res['categories_used'] or 'none'}",
           f"Declared: {res['categories_declared'] or 'none'}", ""]
    order = {"BLOCKER": 0, "WARN": 1, "INFO": 2}
    for f in sorted(res["findings"], key=lambda x: order[x["severity"]]):
        out.append(f"[{f['severity']}] {f['code']}: {f['message']}" + (f"  @ {f['where']}" if f.get("where") else ""))
    if not res["findings"]:
        out.append("No findings.")
    out.append("")
    out.append("Declare only reasons that are true for how the code uses the API; an accepted upload is not proof the reason is right.")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], epilog="Exit codes: 0 clean, 2 warnings, 3 bad input, 4 blocked.")
    ap.add_argument("--project", help="iOS project root (folder with the .xcodeproj or Package.swift)")
    ap.add_argument("--manifest", help="app PrivacyInfo.xcprivacy, when the project has several")
    ap.add_argument("--sample", action="store_true", help="run on a built-in sample project")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    if a.sample:
        import tempfile
        tmp = tempfile.mkdtemp(prefix="ios-sample-")
        write_sample(tmp)
        root = tmp
    elif a.project:
        root = os.path.abspath(a.project)
        if not os.path.isdir(root):
            print(f"error: {a.project} is not a directory", file=sys.stderr)
            return EXIT["BAD_INPUT"]
    else:
        ap.print_usage(sys.stderr)
        print("error: give --project DIR or --sample", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    try:
        res = check(root, a.manifest)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    print(json.dumps(res, indent=2) if a.output == "json" else render(res))
    return EXIT[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
