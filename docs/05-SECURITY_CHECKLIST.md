# 🔒 Claude Skills Security Verification Checklist

**Amaç:** Her skill'i production environment'a koymadan önce güvenlik kontrolü yapma  
**Zorunlu:** Evet - her skill için bağımsız olarak uygulanmalı  
**Ortalama Süre:** Skill başına 5-10 dakika

---

## 📋 PRE-INSTALLATION SECURITY MATRIX

### Tier 1: İLK BAKIŞ KONTROLLERI (Tüm skills)

```
☐ Source Verification
   └─ Kaynağı doğru mu? (official, verified community, trusted)
   └─ GitHub link çalışıyor mu?
   └─ README'de açık açıklamalar var mı?

☐ File Type Check
   └─ .md file mi? (expected)
   └─ Suspicious extensions (.exe, .sh, .py, .bin)?
   └─ Binary file mi? (should be text only)

☐ File Size Analysis
   └─ Size normal mi? (> 10MB ise şüpheli)
   └─ Compressed/obfuscated content var mı?
```

---

## 🔍 CONTENT ANALYSIS - DETAILED SECURITY CHECKS

### Check #1: Malicious Code Patterns

**String Patterns'ı Ara:**
```bash
# Terminal command kullanarak tarama:
grep -E "(eval|exec|system|shell|spawn|fork|rm -rf|:(){)" skill-file.md

# Eğer HERHANGI BIR match varsa:
🚫 REJECT - Manual review gerekli
```

**Tehlikeli Keywords:**
```
⚠️ eval() - dinamik kod çalıştırma
⚠️ exec() - shell command'ları
⚠️ __import__ - module injection
⚠️ subprocess - external process
⚠️ os.system - sistem komutları
⚠️ socket - network access
⚠️ open/read file operations - sensitive files
⚠️ API keys, passwords, tokens
```

### Check #2: Permissions & Access Control

```
☐ Skill, Claude'a tam project access talep ediyor mu?
   └─ YES: Gerekçe açık mı?
   └─ NO: İyi sign - limited scope

☐ Sensitive file/directory access?
   └─ ~/.ssh/ - SSH keys?
   └─ ~/.aws/ - AWS credentials?
   └─ ~/.env - Environment variables?
   └─ Home directory'ye erişim?

☐ External API calls?
   └─ API key'leri locally store ediyor mu?
   └─ Hardcoded credentials var mı?
   └─ HTTPS konusunda guarantee var mı?
```

### Check #3: Dependencies Analysis

```
☐ External packages/imports?
   └─ List et: [Package1, Package2, ...]
   └─ Tüm packages reputable mi?
   └─ Version pinned mi? (security)
   └─ Known vulnerabilities kontrol et (npm audit, pip check)

☐ Network Connections?
   └─ Hangi domains'e bağlanıyor?
   └─ API endpoints güvenli mi?
   └─ Rate limiting var mı?

☐ Data Handling?
   └─ Logging yapıyor mu? (sensitive data leak risk)
   └─ Data encryption uygulanmış mı?
   └─ Data retention policy var mı?
```

---

## 📝 SKILL-SPECIFIC VERIFICATION TEMPLATES

### Template A: OFFICIAL SKILLS (Anthropic, Google, Vercel, etc.)

**Green Light Criteria:**
```
✅ Resmi GitHub repository
✅ Anthropic/Google/Vercel official marca
✅ Maintained status (recent commits)
✅ Clear documentation
✅ No security advisories
✅ 100+ stars (community trust)

Kontrol adımları:
1. GitHub page'ini ziyaret et
2. About sektion'unu oku
3. Security policy kontrol et
4. Recent issues/PRs gözden geçir
5. License type verify et
```

**Red Flags:**
```
🚫 Forked from unknown source
🚫 No recent activity (1+ yıl)
🚫 Open security issues
🚫 Controversial license
🚫 Closed issues with complaints
```

### Template B: COMMUNITY CONTRIBUTIONS

**Research Checklist:**
```
☐ Creator's reputation check
   └─ GitHub profile age: ___ (1+ yıl ideal)
   └─ Contribution history: ___ (active?)
   └─ Follows: ___ (beklenmedik accounts?)

☐ Code quality indicators
   └─ Format clean mi?
   └─ Comments açıklayıcı mı?
   └─ Tests written mi?
   └─ Error handling var mı?

☐ Community feedback
   └─ Stars count: ___
   └─ Forks count: ___
   └─ Open issues: ___
   └─ PR history: ___
   
Risk Assessment:
- High: < 10 stars, new creator, no tests
- Medium: 10-100 stars, some activity
- Low: 100+ stars, active maintainer, good tests
```

### Template C: INTERNAL/CUSTOM SKILLS

```
☐ Internal review completed
   └─ Author authorized
   └─ Code reviewed
   └─ Tested in staging

☐ Company policies compliant
   └─ Data handling policy
   └─ API usage policy
   └─ Security standards

☐ Documentation complete
   └─ Purpose açık
   └─ Usage examples
   └─ Troubleshooting
   └─ Maintenance plan
```

---

## 🛡️ STEP-BY-STEP VERIFICATION PROCESS

### Aşama 1: Pre-Download (2 dakika)

```bash
# 1. GitHub page'ini aç
# 2. Şu kontrolleri yap:

Repository Stats Check:
- Repository created: ___ (age)
- Last update: ___ (how recent?)
- Total commits: ___
- Branches: (main stable mi?)
- Tags/Releases: (versioned mı?)

Ownership Verification:
- Owner profile: [name]
- Organization affiliation: ___
- Verification badge: ☐ Yes ☐ No

License Review:
- License type: ___ (MIT, Apache, GPL, etc.)
- License compatible: ☐ Yes ☐ No
- Patent clauses: ☐ None ☐ Present
```

### Aşama 2: Download & Local Scan (3 dakika)

```bash
# Terminal'de:

# 1. Raw content indir
curl -o skill-check.md https://raw.githubusercontent.com/...

# 2. Quick scan
file skill-check.md          # file type verify
wc -l skill-check.md         # line count (excessive?)
head -50 skill-check.md      # start scanning
tail -50 skill-check.md      # end scanning

# 3. Pattern arama (ONE-LINER - execute et!)
grep -iE "(eval|exec|system|shell|spawn|fork|credentials|password|apikey|secret)" skill-check.md

# Eğer result varsa: 🚫 STOP - Further analysis needed

# 4. Size check
ls -lh skill-check.md        # Normal: < 500KB
                             # Suspicious: > 5MB
```

### Aşama 3: Content Deep Dive (5 dakika)

**Editor'de aç ve gözden geçir:**

```markdown
Section-by-Section Review:

1. HEADER SECTION
   ☐ Title açık mı?
   ☐ Author listed mı?
   ☐ Date added?
   ☐ Purpose clear?

2. DESCRIPTION
   ☐ What does it do?
   ☐ Why needed?
   ☐ Use cases?
   ☐ Limitations?

3. INSTALLATION
   ☐ Steps simple?
   ☐ Any suspicious commands?
   ☐ Dependencies listed?
   ☐ Version specified?

4. USAGE/EXAMPLES
   ☐ Examples executable?
   ☐ API calls documented?
   ☐ Error handling shown?
   ☐ Security notes present?

5. CONFIGURATION
   ☐ env variables needed?
   ☐ Credentials required?
   ☐ How to secure them?
   ☐ Default values safe?

6. CODE/COMMANDS (if included)
   ☐ No shell commands?
   ☐ No file operations?
   ☐ No network requests?
   ☐ No API key hardcoding?

7. DEPENDENCIES
   ☐ All listed?
   ☐ Versions specified?
   ☐ Known issues?
   ☐ Alternatives mentioned?

8. LICENSE/ATTRIBUTION
   ☐ License stated?
   ☐ Authors credited?
   ☐ Compatible with our license?
```

---

## ✅ FINAL DECISION MATRIX

**Use this to make go/no-go decision:**

```
DECISION TREE:

1. Is it from official source (Anthropic/Google/Vercel)?
   YES → Go to step 4
   NO → Continue to step 2

2. Does it have:
   - 50+ stars?
   - Active maintenance?
   - Clear documentation?
   All YES → Go to step 4
   Any NO → Go to step 3

3. Manual deep review:
   - Read 100% of code
   - Check creator reputation
   - Look for red flags
   - Ask in community
   Decision: ☐ APPROVE ☐ REJECT

4. Final security checklist:
   ☐ No malicious patterns
   ☐ No credential exposure
   ☐ No suspicious permissions
   ☐ Dependencies safe
   ☐ License compatible
   
   All checked → APPROVED ✅
   Any issue → HOLD FOR REVIEW 🔶
```

---

## 📊 APPROVAL LEVELS

### TIER 1: AUTO-APPROVED (Green Light)
```
✅ APPROVED WITHOUT REVIEW:
- Anthropic official skills
- Google official skills
- Vercel/Stripe/Cloudflare official
- 500+ stars, active maintenance
- Clear security policy
- No security advisories
```

### TIER 2: STANDARD REVIEW (Yellow Light)
```
🔶 REVIEW REQUIRED (20 dakika):
- 50-500 stars
- Active maintainer (< 6 months)
- Clear documentation
- No major red flags
- Community feedback positive
```

### TIER 3: DEEP REVIEW (Red Light)
```
🚫 ENHANCED REVIEW (1+ saat):
- New/unknown creator
- Few stars/forks
- No clear maintenance
- Suspicious patterns
- Multiple red flags
- Requires security team approval
```

### TIER 4: BLOCKED (Do Not Use)
```
❌ REJECTED:
- Malicious code detected
- Hardcoded credentials
- Inactive/abandoned
- Controversial license
- Security issues reported
- Cannot contact creator
```

---

## 📋 DOCUMENTATION TEMPLATE - Her Skill İçin

**Create a security-audit.txt file for each skill:**

```
=== SECURITY AUDIT REPORT ===
Skill Name: _______________
Date Reviewed: _______________
Reviewed By: _______________

TIER CLASSIFICATION: ☐ 1 ☐ 2 ☐ 3 ☐ 4

SOURCE VERIFICATION:
- Repository: _______________
- Creator: _______________
- Stars/Forks: ___ / ___
- Last Update: _______________

CONTENT SCAN:
- Malicious patterns: ☐ None ☐ Found ☐ Suspicious
- Credentials exposed: ☐ No ☐ Yes (list)
- File operations: ☐ Safe ☐ Risky
- Network access: ☐ None ☐ Documented ☐ Undocumented

DEPENDENCIES:
- Count: ___
- All verified: ☐ Yes ☐ No
- Known vulnerabilities: ☐ None ☐ Found (list)

PERMISSIONS REQUIRED:
- Project access level: ☐ Limited ☐ Full
- Sensitive file access: ☐ No ☐ Yes (list)
- API keys needed: ☐ No ☐ Yes (list)

DECISION:
☐ APPROVED - Safe to use
☐ APPROVED WITH CAUTION - Use in controlled environment
☐ REJECTED - Do not use
☐ HOLD - Awaiting additional review

Notes/Concerns:
___________________________________
___________________________________

Signature: _______________ Date: _______
```

---

## 🚀 QUICK REFERENCE COMMAND

**Tek komutla quick security check:**

```bash
#!/bin/bash
# File: check-skill-security.sh

SKILL_FILE=$1

echo "🔍 QUICK SECURITY SCAN: $SKILL_FILE"
echo "=================================="

echo "1️⃣ Checking for malicious patterns..."
RESULTS=$(grep -iE "(eval|exec|system|shell|spawn|fork|rm -rf)" "$SKILL_FILE" | wc -l)
if [ $RESULTS -gt 0 ]; then
    echo "⚠️ WARNING: Found $RESULTS suspicious patterns"
else
    echo "✅ No obvious malicious patterns"
fi

echo ""
echo "2️⃣ Checking for credentials..."
CREDS=$(grep -iE "(password|apikey|secret|token|credential)" "$SKILL_FILE" | wc -l)
if [ $CREDS -gt 0 ]; then
    echo "⚠️ WARNING: Found $CREDS credential-related strings"
    grep -iE "(password|apikey|secret|token)" "$SKILL_FILE"
else
    echo "✅ No obvious credentials"
fi

echo ""
echo "3️⃣ File stats..."
SIZE=$(ls -lh "$SKILL_FILE" | awk '{print $5}')
LINES=$(wc -l < "$SKILL_FILE")
echo "Size: $SIZE | Lines: $LINES"

if [[ "$SIZE" > "500K" ]] || [[ "$LINES" > "10000" ]]; then
    echo "⚠️ File unusually large"
fi

echo ""
echo "✅ Quick scan complete. Review results above!"
```

**Kullanım:**
```bash
bash check-skill-security.sh skill-file.md
```

---

## 🎯 CHECKLIST - KURULUMA GİDEN ÖNCESİ

```
Final Go/No-Go Decision:

☐ Source verification complete
☐ Content scan passed
☐ Dependencies validated
☐ Permissions acceptable
☐ License compatible
☐ Security audit signed off
☐ Documentation reviewed
☐ Team approval obtained (if required)
☐ Backup created before installation
☐ Rollback plan ready

ALL CHECKED ✅ → PROCEED TO INSTALLATION
ANY UNCHECKED 🔶 → HOLD FOR REVIEW
```

---

## 📞 ESCALATION PROCESS

**Eğer herhangi bir şüphe varsa:**

```
1. Ask in community:
   - GitHub discussions
   - Discord/Slack communities
   - Reddit: r/claudeai

2. Create security issue:
   - If on GitHub: Open issue with [SECURITY] tag
   - Ask creator for clarification

3. Team review:
   - Bring to security team
   - Request formal audit
   - Document decision

4. When in doubt:
   🎯 DO NOT INSTALL
   Better safe than sorry!
```

---

## 📈 METRICS TO TRACK

```
Monthly Security Report:

Skills Reviewed: ___
Auto-Approved: ___ (%)
Standard Review: ___ (%)
Deep Review: ___ (%)
Rejected: ___ (%)

Issues Found:
- Malicious patterns: ___
- Credential exposure: ___
- Suspicious permissions: ___

Time Average:
- Auto-review: ___ mins
- Standard review: ___ mins
- Deep review: ___ mins
```

---

**Remember: Security is NOT optional. Every skill needs review. 🔒**

*Last updated: June 2026*  
*Version: 1.0*
