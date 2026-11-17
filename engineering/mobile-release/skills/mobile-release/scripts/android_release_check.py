#!/usr/bin/env python3
"""Check an Android project against Google Play's release rules before upload.

Reads the Gradle build files and AndroidManifest.xml files of a project
(native, React Native, Flutter or Capacitor) and reports what would stop or
delay a Play release.

Findings
  TARGET_SDK_TOO_LOW    targetSdk below Play's level for new apps and updates
                        on the given date and form factor                   BLOCKER
  NOT_DISCOVERABLE      existing app below the level that keeps it visible to
                        new users on newer devices                           WARN
  EXPORTED_MISSING      component with an intent-filter and no
                        android:exported, targetSdk >= 31 (install fails)    BLOCKER
  DEBUGGABLE            android:debuggable="true" in a release manifest      BLOCKER
  CLEARTEXT_TRAFFIC     android:usesCleartextTraffic="true"                  WARN
  EXPORTED_UNPROTECTED  exported service/receiver/provider with no
                        android:permission                                   WARN
  DECLARATION_REQUIRED  permission that needs a Play Console declaration form
                        or policy review before release                      WARN
  PAGE_SIZE_16KB        native code and targetSdk >= 35: must support 16 KB
                        pages; updates without it are refused from
                        2027-02-01                                           WARN
  DATA_SAFETY_REVIEW    sensitive permission: check the Data safety form
                        declares the matching data type                     INFO

targetSdk is read from build.gradle(.kts), gradle.properties,
variables.gradle (Capacitor), libs.versions.toml or the manifest. When it is
set through a variable this script cannot resolve, pass --target-sdk.

Exit codes: 0 clean, 2 warnings only, 3 bad input, 4 blocked.
Rules verified against developer.android.com on 2026-11-17; re-check the Play
Console Help page for dates after that.
Deterministic, stdlib only, no network.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

RULES_VERIFIED = "2026-11-17"
EXIT = {"CLEAN": 0, "WARNINGS": 2, "BAD_INPUT": 3, "BLOCKED": 4}
ANDROID_NS = "{http://schemas.android.com/apk/res/android}"
SKIP_DIRS = {".git", "build", "node_modules", ".gradle", ".dart_tool", "Pods", "ios"}

# (effective_from, new_and_updates by form factor, existing apps visible to new users, extension_until)
TARGET_RULES = [
    (dt.date(2026, 8, 31),
     {"phone": 36, "tablet": 36, "wear": 35, "automotive": 35, "tv": 34, "xr": 34},
     35, dt.date(2026, 11, 1)),
]
PAGE_SIZE_DEADLINE = dt.date(2027, 2, 1)

DECLARATION = {
    "android.permission.READ_SMS": "SMS and Call Log permissions policy: declaration form, allowed only for default handlers or listed exceptions",
    "android.permission.SEND_SMS": "SMS and Call Log permissions policy",
    "android.permission.RECEIVE_SMS": "SMS and Call Log permissions policy",
    "android.permission.RECEIVE_MMS": "SMS and Call Log permissions policy",
    "android.permission.READ_CALL_LOG": "SMS and Call Log permissions policy",
    "android.permission.WRITE_CALL_LOG": "SMS and Call Log permissions policy",
    "android.permission.PROCESS_OUTGOING_CALLS": "SMS and Call Log permissions policy",
    "android.permission.ACCESS_BACKGROUND_LOCATION": "location permissions declaration with a video of the feature",
    "android.permission.MANAGE_EXTERNAL_STORAGE": "All files access declaration",
    "android.permission.QUERY_ALL_PACKAGES": "package visibility (broad app visibility) declaration",
    "android.permission.REQUEST_INSTALL_PACKAGES": "request install packages declaration",
    "android.permission.USE_EXACT_ALARM": "exact alarm policy: only for alarm, timer or calendar apps",
    "android.permission.USE_FULL_SCREEN_INTENT": "full-screen intent declaration (calling and alarm apps)",
    "android.permission.BIND_ACCESSIBILITY_SERVICE": "AccessibilityService API declaration",
    "android.permission.BIND_VPN_SERVICE": "VpnService declaration",
    "android.permission.READ_MEDIA_IMAGES": "photo and video permissions policy (use the photo picker unless core)",
    "android.permission.READ_MEDIA_VIDEO": "photo and video permissions policy (use the photo picker unless core)",
}
FGS_PREFIX = "android.permission.FOREGROUND_SERVICE_"
DATA_SAFETY = {
    "android.permission.ACCESS_FINE_LOCATION": "Location: precise location",
    "android.permission.ACCESS_COARSE_LOCATION": "Location: approximate location",
    "android.permission.ACCESS_BACKGROUND_LOCATION": "Location (background)",
    "android.permission.READ_CONTACTS": "Contacts",
    "android.permission.READ_CALENDAR": "Calendar events",
    "android.permission.RECORD_AUDIO": "Audio: voice or sound recordings (if recordings leave the device)",
    "android.permission.CAMERA": "Photos and videos (if captures leave the device)",
    "android.permission.BODY_SENSORS": "Health and fitness",
    "android.permission.ACTIVITY_RECOGNITION": "Health and fitness: fitness info",
    "android.permission.READ_PHONE_STATE": "Device or other IDs",
    "android.permission.GET_ACCOUNTS": "Personal info: email address / user IDs",
}

SAMPLE = {
    "app/build.gradle.kts": 'android {\n  namespace = "com.example.app"\n  defaultConfig {\n    minSdk = 24\n    targetSdk = 35\n  }\n  externalNativeBuild { cmake { path = file("src/main/cpp/CMakeLists.txt") } }\n}\n',
    "app/src/main/AndroidManifest.xml": (
        '<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n'
        '  <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>\n'
        '  <uses-permission android:name="android.permission.ACCESS_BACKGROUND_LOCATION"/>\n'
        '  <uses-permission android:name="android.permission.FOREGROUND_SERVICE_LOCATION"/>\n'
        '  <application android:usesCleartextTraffic="true">\n'
        '    <activity android:name=".MainActivity" android:exported="true">\n'
        '      <intent-filter><action android:name="android.intent.action.MAIN"/></intent-filter>\n'
        '    </activity>\n'
        '    <receiver android:name=".BootReceiver">\n'
        '      <intent-filter><action android:name="android.intent.action.BOOT_COMPLETED"/></intent-filter>\n'
        '    </receiver>\n'
        '  </application>\n'
        '</manifest>\n'),
}


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            yield os.path.join(dirpath, name)


def read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def find_sdk(files, root):
    """Return {'targetSdk': int|None, 'minSdk': ..., 'source': ...}."""
    found = {}
    gradle = [f for f in files if f.endswith((".gradle", ".gradle.kts"))]
    props = [f for f in files if f.endswith(("gradle.properties", "libs.versions.toml"))]
    var_pat = re.compile(r"\b(targetSdk(?:Version)?|minSdk(?:Version)?|compileSdk(?:Version)?)\b\s*[=:]?\s*\(?\s*([\w.\[\]'\"$]+)")
    variables = {}
    for f in gradle + props:
        for m in re.finditer(r"\b([A-Za-z_][\w.-]*)\s*=\s*['\"]?(\d{2})['\"]?\s*$", read(f), re.M):
            variables[m.group(1)] = int(m.group(2))
    for f in sorted(gradle, key=lambda p: ("app" not in p.split(os.sep), p)):
        for m in var_pat.finditer(read(f)):
            key = m.group(1).replace("Version", "")
            raw = m.group(2).strip("'\"()")
            val = int(raw) if raw.isdigit() else None
            if val is None:
                tail = re.split(r"[.\[]", raw.replace("]", "").replace("'", "").replace('"', ""))[-1]
                val = variables.get(tail) or variables.get(raw)
            if key not in found and val is not None:
                found[key] = (val, os.path.relpath(f, root))
    return found


def elf_min_load_align(path):
    """Smallest p_align of PT_LOAD segments in an ELF file, or None if not ELF."""
    import struct
    try:
        with open(path, "rb") as fh:
            head = fh.read(64)
            if head[:4] != b"\x7fELF":
                return None
            is64 = head[4] == 2
            end = "<" if head[5] == 1 else ">"
            if is64:
                phoff, = struct.unpack(end + "Q", head[32:40])
                phentsize, phnum = struct.unpack(end + "HH", head[54:58])
            else:
                phoff, = struct.unpack(end + "I", head[28:32])
                phentsize, phnum = struct.unpack(end + "HH", head[42:46])
            aligns = []
            for i in range(phnum):
                fh.seek(phoff + i * phentsize)
                ph = fh.read(phentsize)
                ptype, = struct.unpack(end + "I", ph[:4])
                if ptype != 1:
                    continue
                align = struct.unpack(end + "Q", ph[48:56])[0] if is64 else struct.unpack(end + "I", ph[28:32])[0]
                aligns.append(align)
            return min(aligns) if aligns else None
    except (OSError, struct.error):
        return None


def find_manifests(files):
    return [f for f in files if os.path.basename(f) == "AndroidManifest.xml"
            and ("src" + os.sep + "debug") not in f and ("src" + os.sep + "androidTest") not in f]


def rule_for(date):
    rule = None
    for r in TARGET_RULES:
        if date >= r[0]:
            rule = r
    return rule


def check(root, form, on, target_override=None):
    findings = []

    def add(sev, code, msg, where=None):
        findings.append({"severity": sev, "code": code, "message": msg, "where": where})

    files = list(walk(root))
    sdk = find_sdk(files, root)
    manifests = find_manifests(files)
    if not manifests and not sdk:
        raise ValueError("no Gradle files or AndroidManifest.xml found; point --project at the Android project (the folder with settings.gradle)")
    perms = set()
    for mf in manifests:
        rel = os.path.relpath(mf, root)
        try:
            tree = ET.parse(mf).getroot()
        except ET.ParseError as exc:
            raise ValueError(f"cannot parse {rel}: {exc}")
        uses_sdk = tree.find("uses-sdk")
        if uses_sdk is not None and "targetSdk" not in sdk:
            v = uses_sdk.get(ANDROID_NS + "targetSdkVersion")
            if v and v.isdigit():
                sdk["targetSdk"] = (int(v), rel)
        for up in tree.iter("uses-permission"):
            perms.add(up.get(ANDROID_NS + "name", ""))
        for up in tree.iter("uses-permission-sdk-23"):
            perms.add(up.get(ANDROID_NS + "name", ""))
        app = tree.find("application")
        if app is None:
            continue
        if app.get(ANDROID_NS + "debuggable") == "true":
            add("BLOCKER", "DEBUGGABLE", "android:debuggable=\"true\"; Play rejects debuggable release builds", rel)
        if app.get(ANDROID_NS + "usesCleartextTraffic") == "true":
            add("WARN", "CLEARTEXT_TRAFFIC", "cleartext HTTP allowed app-wide; scope it with a network security config instead", rel)
        for kind in ("activity", "activity-alias", "service", "receiver", "provider"):
            for comp in app.iter(kind):
                name = comp.get(ANDROID_NS + "name", "?")
                exported = comp.get(ANDROID_NS + "exported")
                has_filter = comp.find("intent-filter") is not None
                comp_tag = f"<{kind} {name}>"
                if has_filter and exported is None:
                    comp_tag_msg = f"{comp_tag} has an intent-filter and no android:exported"
                    findings.append({"severity": "PENDING_EXPORTED", "code": "EXPORTED_MISSING", "message": comp_tag_msg, "where": rel})
                if exported == "true" and kind in ("service", "receiver", "provider") and not comp.get(ANDROID_NS + "permission"):
                    add("WARN", "EXPORTED_UNPROTECTED", f"{comp_tag} is exported with no android:permission; any app can call it", rel)

    target = target_override if target_override is not None else (sdk.get("targetSdk", (None, None))[0])
    target_src = "--target-sdk" if target_override is not None else sdk.get("targetSdk", (None, None))[1]
    if target is None:
        raise ValueError("targetSdk not found or set through a variable this script cannot resolve; pass --target-sdk N")

    for f in findings:
        if f["severity"] == "PENDING_EXPORTED":
            if target >= 31:
                f["severity"] = "BLOCKER"
                f["message"] += "; required from targetSdk 31, the APK will not install"
            else:
                f["severity"] = "INFO"
                f["message"] += "; set it before raising targetSdk to 31+"

    rule = rule_for(on)
    rule_info = None
    if rule is None:
        add("INFO", "NO_RULE_FOR_DATE", f"this script's rule table starts {TARGET_RULES[0][0]}; check the Play Console Help page for {on}")
    else:
        start, levels, existing, ext = rule
        need = levels[form]
        rule_info = {"effective_from": str(start), "required_for_new_and_updates": need, "existing_visible_to_new_users": existing, "extension_until": str(ext)}
        if target < need:
            note = f" (an extension to {ext} can be requested in Play Console)" if on < ext else ""
            add("BLOCKER", "TARGET_SDK_TOO_LOW", f"targetSdk {target} < {need} required for new apps and updates ({form}) since {start}{note}", target_src)
        if target < existing:
            add("WARN", "NOT_DISCOVERABLE", f"targetSdk {target} < {existing}: the live app is hidden from new users on newer Android versions", target_src)

    for p in sorted(perms):
        if p in DECLARATION:
            add("WARN", "DECLARATION_REQUIRED", f"{p.split('.')[-1]}: {DECLARATION[p]}")
        elif p.startswith(FGS_PREFIX):
            add("WARN", "DECLARATION_REQUIRED", f"{p.split('.')[-1]}: foreground service type must be declared in Play Console (App content) with a use-case and video")
        if p in DATA_SAFETY:
            add("INFO", "DATA_SAFETY_REVIEW", f"{p.split('.')[-1]}: Data safety form should cover '{DATA_SAFETY[p]}' if that data is collected or shared")

    sos = [f for f in files if f.endswith(".so")]
    native = bool(sos) or any(
        f.endswith((".gradle", ".gradle.kts")) and re.search(r"externalNativeBuild|ndkVersion|cmake\s*\{|ndkBuild", read(f)) for f in files)
    if native and target >= 35:
        bad = []
        for so in sos:
            align = elf_min_load_align(so)
            if align is not None and align < 16384:
                bad.append(f"{os.path.relpath(so, root)} (align {align})")
        if bad:
            add("WARN", "PAGE_SIZE_16KB", f"{len(bad)} prebuilt .so not 16 KB aligned: {', '.join(bad[:5])}; get 16 KB builds of these libraries. Updates without 16 KB support cannot be released from {PAGE_SIZE_DEADLINE}")
        else:
            add("WARN", "PAGE_SIZE_16KB", f"native code found: build with AGP 8.5.1+ and NDK r28+ and verify the APK with `zipalign -c -P 16 -v 4 app.apk`; updates without 16 KB support cannot be released from {PAGE_SIZE_DEADLINE}")

    blocked = any(x["severity"] == "BLOCKER" for x in findings)
    warned = any(x["severity"] == "WARN" for x in findings)
    return {
        "verdict": "BLOCKED" if blocked else ("WARNINGS" if warned else "CLEAN"),
        "rules_verified": RULES_VERIFIED,
        "date": str(on),
        "form_factor": form,
        "targetSdk": target,
        "targetSdk_source": target_src,
        "minSdk": sdk.get("minSdk", (None,))[0],
        "rule": rule_info,
        "manifests": [os.path.relpath(m, root) for m in manifests],
        "findings": findings,
    }


def render(res):
    out = [f"Android release check: {res['verdict']}  (rules verified {res['rules_verified']}, evaluated for {res['date']}, {res['form_factor']})",
           f"targetSdk {res['targetSdk']} from {res['targetSdk_source']}; minSdk {res['minSdk']}"]
    if res["rule"]:
        r = res["rule"]
        out.append(f"Play rule since {r['effective_from']}: new apps and updates >= {r['required_for_new_and_updates']}; existing apps >= {r['existing_visible_to_new_users']} to stay visible to new users")
    out.append("")
    order = {"BLOCKER": 0, "WARN": 1, "INFO": 2}
    for f in sorted(res["findings"], key=lambda x: order[x["severity"]]):
        out.append(f"[{f['severity']}] {f['code']}: {f['message']}" + (f"  @ {f['where']}" if f.get("where") else ""))
    if not res["findings"]:
        out.append("No findings.")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], epilog="Exit codes: 0 clean, 2 warnings, 3 bad input, 4 blocked.")
    ap.add_argument("--project", help="Android project root (folder with settings.gradle), or the android/ folder of an RN/Flutter/Capacitor app")
    ap.add_argument("--form-factor", choices=["phone", "tablet", "wear", "automotive", "tv", "xr"], default="phone")
    ap.add_argument("--date", help="evaluate the rules on this date, YYYY-MM-DD (default today)")
    ap.add_argument("--target-sdk", type=int, help="targetSdk when the build sets it through an unresolvable variable")
    ap.add_argument("--sample", action="store_true", help="run on a built-in sample project")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    try:
        on = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
    except ValueError:
        print("error: --date must be YYYY-MM-DD", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    if a.sample:
        import tempfile
        root = tempfile.mkdtemp(prefix="android-sample-")
        for rel, text in SAMPLE.items():
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(text)
        if not a.date:
            on = dt.date(2026, 11, 17)
    elif a.project and os.path.isdir(a.project):
        root = os.path.abspath(a.project)
    else:
        print("error: give --project DIR (an existing directory) or --sample", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    try:
        res = check(root, a.form_factor, on, a.target_sdk)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    print(json.dumps(res, indent=2) if a.output == "json" else render(res))
    return EXIT[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
