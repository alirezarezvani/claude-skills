# Contributing to Claude Skills Collection

Katkılarınız için teşekkür ederiz! 🙏

Bu repository'ye katılmak istediğiniz takdirde, lütfen bu rehberi takip edin.

---

## 🤝 Nasıl Katkı Yapabilirim?

### 1. Skills Eklemek

Yeni bir skill eklemek istiyorsanız:

```bash
# Feature branch oluştur
git checkout -b feature/add-skill-name

# skills/ klasöründe yeni dosya oluştur
# Format: SKILL.md (Anthropic specification)

# İçeriği ekle
# - Description
# - Usage examples
# - Requirements
# - Attribution

# Commit et
git add skills/X-collection/skill-name.md
git commit -m "Add: skill-name description"

# Push et
git push origin feature/add-skill-name

# Pull request aç
```

### 2. Belgeleri İyileştirmek

Dokümantasyonda hata bulduysanız:

```bash
git checkout -b fix/documentation-improvement

# Dosyayı düzenle
# docs/ klasöründe değişiklik yap

git add docs/filename.md
git commit -m "Fix: Documentation improvement description"

git push origin fix/documentation-improvement
```

### 3. Scripti Geliştirmek

```bash
git checkout -b feature/script-enhancement

# scripts/ klasöründe değişiklik yap

git add scripts/script-name.sh
git commit -m "Improve: script enhancement description"

git push origin feature/script-enhancement
```

---

## 📋 PULL REQUEST CHECKLIST

PR açmadan önce lütfen kontrol edin:

```
[ ] Branching convention takip edildi? (feature/, fix/, docs/)
[ ] Commit message açıklayıcı mı? (50 char title + body)
[ ] İlgili documentation updated?
[ ] Code/files tested?
[ ] No merge conflicts?
[ ] Attribution added (if external source)?
```

---

## 🔒 SECURITY CONSIDERATIONS

Skill eklerken:

```
[ ] Code reviewed for malicious patterns?
[ ] External dependencies documented?
[ ] Permissions/capabilities listed?
[ ] License compatible with MIT?
[ ] Original author credited?
```

---

## 📝 COMMIT MESSAGE CONVENTION

### Format:

```
Type: Subject (50 chars max)

Body (72 char wrapping):
- What changed
- Why it changed
- Any relevant context

Footer (if needed):
Closes #123
Related-To #456
```

### Types:

- `Add:` Yeni skill/feature
- `Fix:` Bug fix
- `Update:` İmprovement/enhancement
- `Docs:` Documentation only
- `Refactor:` Code reorganization
- `Remove:` Deprecated content

### Examples:

```
Add: Production-ready React component skill

Adds a comprehensive skill for creating production-grade
React components with TypeScript, testing, and documentation.
Includes examples and best practices.

Closes #42

---

Fix: Security checklist formatting issue

Fixed incorrect markdown formatting in SECURITY_CHECKLIST.md
that prevented proper rendering on GitHub.

---

Update: Execution plan timeline

Extended Day 3 timeline based on community feedback.
More realistic estimation for skill installation.
```

---

## 📂 FOLDER STRUCTURE RULES

```
skills/
├── 1-awesome-agent-skills/
├── 2-claude-command-suite/
├── 3-production-ready-commands/
├── 4-awesome-claude-skills/
└── 5-claude-code-settings/

Rules:
✓ Use numbered prefixes (1-, 2-, etc)
✓ Use lowercase-with-hyphens for folders
✓ One skill = one .md file
✓ Include INDEX.md in each folder
✓ Maintain METADATA.json
```

---

## 📄 SKILL TEMPLATE

Yeni skill eklerken bu template'i kullan:

```markdown
---
name: skill-name
description: What this skill does and when to use it
author: Your Name
license: MIT
---

# Skill Name

## Description
[What the skill does, why it's useful]

## Usage
[How to use it]

## Examples
[Real examples]

## Requirements
[Dependencies, prerequisites]

## Notes
[Important considerations]

## Attribution
[Original source if applicable]
```

---

## 🔄 REVIEW PROCESS

1. **Your PR** → Opens on GitHub
2. **Automated Checks** → Format, links, structure
3. **Manual Review** → Content, security, alignment
4. **Feedback** → Comments, suggestions
5. **Revision** → You update PR
6. **Approval** → Merged to main

**Average time:** 2-7 days

---

## ✅ TESTING BEFORE PR

```bash
# Security check
bash scripts/check-skill-security.sh skills/path/to/skill.md

# Format validation
# Check .md is valid markdown

# Link validation
# Verify all links work

# Attribution check
# Verify sources cited
```

---

## 🎯 PRIORITY AREAS

Katkılardan özellikle şunlara açığız:

1. **Missing Documentation**
   - Gaps in execution plan
   - Unclear procedures
   - Missing examples

2. **Security Improvements**
   - Better verification procedures
   - Additional malicious pattern checks
   - Testing recommendations

3. **New Skills**
   - Production-ready tools
   - Enterprise patterns
   - Best practices

4. **Translations**
   - Turkish improvements
   - Other languages
   - Terminology clarification

5. **Automation**
   - Better scripts
   - CI/CD improvement
   - Testing tools

---

## ❌ WHAT NOT TO DO

```
✗ Don't commit to main directly
✗ Don't merge your own PR (wait for review)
✗ Don't include large binary files
✗ Don't remove other people's work
✗ Don't change license without discussion
✗ Don't add commercial/proprietary skills
✗ Don't ignore CONTRIBUTING.md
```

---

## 💬 COMMUNICATION

- **Questions?** Open a GitHub Issue
- **Feature idea?** Create Discussion
- **Bug report?** Open Issue with details
- **Documentation?** Comment on relevant MD file

---

## 🏆 RECOGNITION

Katkıda bulunanlar:

- README.md'de yer alacaklar
- CONTRIBUTORS.md'de listelecekler
- Commit history'de kalacaklar
- Release notes'da acknowledge edilecekler

---

## 📊 CONTRIBUTION LEVELS

```
Level 1: Typo fixes, small improvements
         → Auto-merged after check

Level 2: Documentation updates
         → 2-3 days review

Level 3: New skills, features
         → Full review (5-7 days)

Level 4: Major changes, refactoring
         → Discussion + planning before PR
```

---

## 🚀 GETTING STARTED

```bash
# 1. Fork repository
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/claude-skills-collection.git

# 3. Create feature branch
git checkout -b feature/your-feature

# 4. Make changes
# 5. Test locally
# 6. Commit
git add .
git commit -m "Add: your feature description"

# 7. Push to your fork
git push origin feature/your-feature

# 8. Create Pull Request on GitHub
# 9. Wait for review
# 10. Address feedback
# 11. Merge! 🎉
```

---

## 📞 HELP & SUPPORT

Takılırsanız:

1. **Check existing issues/discussions**
2. **Review CONTRIBUTING.md** (this file)
3. **Ask in Issues** with details
4. **Check documentation** in docs/

---

## 📋 CODE OF CONDUCT

Bu repository'ye katkı yapan herkes:

- ✅ Respectful olacak
- ✅ Inclusive olacak
- ✅ Professional olacak
- ✅ Diğer katkıcılara saygılı olacak

Harassment, discrimination, inappropriate behavior → **WILL BE BANNED**

---

## 🎉 THANK YOU!

Katkılarınız bu repository'yi daha iyi yapmaktadır.

**Happy contributing!** 🚀

---

*CONTRIBUTING.md - Contribution Guidelines*  
*Last Updated: June 2026*
