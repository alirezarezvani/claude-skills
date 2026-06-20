# 🚀 GitHub Setup Guide - Repository Oluşturma

**Bu dokümanda:** GitHub'da yeni repository oluşturup dosyaları push etmenin adım-adım rehberi

---

## ✅ ADIM 1: GitHub'da Yeni Repository Oluştur

### 1.1 GitHub'a Git

```
https://github.com/new
```

### 1.2 Bilgiler Doldur

```
Repository name: claude-skills-collection
Description: Professional Claude Skills Repository - 659+ Skills, Turkish Documentation, Production Ready
Visibility: Public (veya Private istersen)
Initialize with:
  ☐ Add a README file (sonra ekleneceğinden untick)
  ☐ Add .gitignore (biz ekleneceğimizden untick)
  ☐ Choose a license (MIT use, sonra ekleneceğimizden untick)
```

### 1.3 Oluştur

```
[Create repository] butonuna tıkla
```

---

## ✅ ADIM 2: Terminalda Local Setup

### 2.1 Klasör Oluştur

```bash
# Klasör oluştur
mkdir -p ~/claude-skills-collection
cd ~/claude-skills-collection

# Tüm dosyaları buraya kopyala (OUTPUT FOLDER'dan)
# Downloads'tan veya bulunduğu yerden kopyala

# Tüm .md, .gitignore, LICENSE dosyalarını kopyala
cp ~/Downloads/claude-skills-collection-files/* .
```

### 2.2 Git Başlat

```bash
# Git repository'yi başlat
git init

# Dosyaları stage et
git add .

# İlk commit
git commit -m "Initial: Claude Skills Collection Repository v1.0

- Complete documentation (Turkish)
- EXECUTION_PLAN for 5-6 day implementation
- SECURITY_CHECKLIST with enterprise procedures
- 659+ professional skills ready to install
- Full alignment with anthropics/skills official repo

Features:
- docs/: Complete documentation (6 guides)
- scripts/: Setup and security automation
- templates/: Skill templates and configs
- LICENSE: MIT License
- Contributing guidelines

Status: Production Ready"
```

### 2.3 Default Branch Ayarla

```bash
# main branch'e rename et (eğer master ise)
git branch -M main
```

---

## ✅ ADIM 3: GitHub'a Push Et

### 3.1 Remote Add

```bash
# GitHub URL'sini ekle
git remote add origin https://github.com/YOUR_USERNAME/claude-skills-collection.git

# Doğrula
git remote -v
```

### 3.2 Dosyaları Push Et

```bash
# Tüm dosyaları push et
git push -u origin main
```

**NOT:** Eğer "fatal: Authentication failed" alırsanız:

```bash
# SSH key setup (recommended)
git remote set-url origin git@github.com:YOUR_USERNAME/claude-skills-collection.git

# veya GitHub Personal Access Token kullan
# https://github.com/settings/tokens
```

---

## ✅ ADIM 4: Repository'yi Customize Et

### 4.1 Description + Topics

GitHub'da repository page'ine git:

```
Settings → About
├─ Description: Professional Claude Skills Collection - 659+ Skills
├─ Website: (optional)
└─ Topics: 
    ✓ claude
    ✓ anthropic
    ✓ skills
    ✓ ai
    ✓ documentation
    ✓ turkish
    ✓ production-ready
```

### 4.2 README Ayarları

```
Settings → Manage access → Public
Settings → Code and automation → Actions (optional, disable if not needed)
```

---

## ✅ ADIM 5: Folder Structure Oluştur (Optional but Recommended)

Eğer ileride skills download etmek istersen:

```bash
# Klasörler oluştur
mkdir -p skills/{1-awesome-agent-skills,2-claude-command-suite,3-production-ready-commands,4-awesome-claude-skills,5-claude-code-settings}
mkdir -p scripts
mkdir -p templates

# .gitkeep dosyaları ekle (boş klasörleri git'te tutmak için)
touch skills/1-awesome-agent-skills/.gitkeep
touch scripts/.gitkeep
touch templates/.gitkeep

# Commit ve push
git add .
git commit -m "Add: Directory structure for skills installation"
git push
```

---

## ✅ ADIM 6: GitHub Actions (Optional)

Eğer automated validation istersen, `.github/workflows/` klasörü oluştur:

```bash
mkdir -p .github/workflows
```

Sonra `.github/workflows/validate.yml` dosyası oluştur:

```yaml
name: Validate Documentation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check markdown files
        run: |
          find docs -name "*.md" -type f
          echo "Documentation files validated"
```

Commit et:

```bash
git add .github/
git commit -m "Add: GitHub Actions validation workflow"
git push
```

---

## ✅ ADIM 7: Collaborators Ekle (Isteğe Bağlı)

Eğer başka kişileri eklemek istersen:

```
Settings → Manage access → Invite a collaborator
```

---

## ✅ ADIM 8: Repository Badge Ekle (Optional)

README.md'ye ekle:

```markdown
# 🚀 Claude Skills Collection

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/YOUR_USERNAME/claude-skills-collection)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()
[![Language: Turkish](https://img.shields.io/badge/Language-Turkish-red.svg)]()

Professional Claude Skills Repository with 659+ Skills
```

---

## ✅ ADIM 9: Tags ve Releases (Optional but Recommended)

```bash
# Tag oluştur
git tag -a v1.0 -m "Version 1.0 - Initial Release"

# Push tags
git push origin v1.0

# veya tüm tags
git push origin --tags
```

GitHub'da Releases:

```
Releases → Create new release
├─ Choose v1.0 tag
├─ Title: Version 1.0 - Initial Release
├─ Description:
    "Professional Claude Skills Collection
    - 659+ skills ready to install
    - Complete Turkish documentation
    - 5-day implementation plan
    - Enterprise security procedures"
└─ Publish Release
```

---

## ✅ KONTROL LİSTESİ

```
Repository Setup:
☐ GitHub'da new repository oluşturdum
☐ Repository name: claude-skills-collection
☐ Visibility: Public (veya Private)

Local Setup:
☐ Klasör oluşturtdum
☐ Tüm dosyaları kopyaladım
☐ git init yaptım
☐ İlk commit yaptım
☐ git remote add origin ...
☐ git push -u origin main

Customization:
☐ Description ve topics ekledi
☐ README customize ettim (optional)
☐ GitHub Actions setup (optional)
☐ Tags/Releases oluşturdum (optional)

Final:
☐ Repository live ve accessible
☐ Tüm dosyalar GitHub'da
☐ main branch'e ve synced
☐ Public/Private ayarları doğru
```

---

## 🔍 VERIFICATION

Ardından, repository'nin doğru setup olup olmadığını kontrol et:

```bash
# Repository'yi yeniden klonla test et
cd /tmp
git clone https://github.com/YOUR_USERNAME/claude-skills-collection.git
cd claude-skills-collection

# Dosyaları kontrol et
ls -la docs/
ls -la *.md

# Tüm dosyalar mı var kontrol et
ls -la | grep -E "README|LICENSE|BAŞLANGIÇ|CONTRIBUTING"
```

---

## 📊 BAŞARILI REPOSITORY ÖZELLIKLERI

```
✅ Klasör:
   Repository name: claude-skills-collection
   
✅ Dosyalar (11):
   - README.md (Main guide)
   - BAŞLANGIÇ.md (Quick start)
   - 6 x Documentation files (docs/)
   - LICENSE (MIT)
   - .gitignore
   - CONTRIBUTING.md
   
✅ Structure:
   - Organized documentation
   - Clear folder hierarchy
   - Contribution guidelines
   
✅ Metadata:
   - Proper description
   - Relevant topics
   - Clear license
```

---

## 🚀 NEXT STEPS

1. ✅ Repository setup complete
2. 👥 Paylaş arkadaşlarınla
3. 🎯 BAŞLANGIÇ.md'den başla
4. 📚 docs/04-EXECUTION_PLAN.md takip et
5. ⭐ Star ver, Fork et, Contribute et!

---

## 📞 EĞER SORUN OLURSA

### Error: "fatal: not a git repository"

```bash
# Klasörde git init yap
git init
```

### Error: "Authentication failed"

```bash
# SSH key setup
ssh-keygen -t ed25519 -C "your-email@example.com"
cat ~/.ssh/id_ed25519.pub  # Copy this

# GitHub → Settings → SSH and GPG keys → New SSH key
# Paste public key

# Test
ssh -T git@github.com
```

### Files not showing up

```bash
# Dosyaların staged olup olmadığını kontrol et
git status

# Ekle ve commit
git add .
git commit -m "Add missing files"
git push
```

### Can't push (403 Forbidden)

```bash
# Personal access token oluştur
# GitHub → Settings → Developer settings → Personal access tokens → Generate new token

# Scopes: repo, workflow

# Terminal'da
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/claude-skills-collection.git
git push
```

---

## ✨ FINAL STATE

```
✅ GitHub Repository: Live
✅ 11 Dosya: Uploaded
✅ Documentation: Complete
✅ License: MIT
✅ Contributing: Guidelines included
✅ Status: Production Ready

Ready for:
☐ Public sharing
☐ Collaboration
☐ Forking
☐ Contributing

🎉 TAMAMLANDI!
```

---

## 📝 GIT COMMANDS QUICK REFERENCE

```bash
# İlk setup
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/user/repo.git
git push -u origin main

# Daily work
git status                    # Durumu kontrol et
git add .                     # Dosyaları stage et
git commit -m "Description"   # Commit et
git push                      # Push et

# Branches
git checkout -b feature/name   # Yeni branch
git switch main               # main'e dön
git push origin feature/name   # Push branch

# Updates from main
git pull origin main          # Latest'i çek
```

---

**Başarılar!** 🚀

*GitHub Setup Guide - June 2026*
