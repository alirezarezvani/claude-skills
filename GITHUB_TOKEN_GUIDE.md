# 🔑 GITHUB PERSONAL ACCESS TOKEN OLUŞTURMA
## Adım-Adım Rehberi (5 dakika)

---

## 📱 STEP 1: GitHub'a Giriş Yap

```
1. Tarayıcında:
   https://github.com

2. Sağ üst köşe: Profil resmi → Click
3. Açılan menu'da: "Sign in" (eğer değilse) 
4. Username + Password ile giriş yap
```

---

## ⚙️ STEP 2: Settings'e Git

```
1. Profil resmi → Click
2. "Settings" → Click

(Direct link: https://github.com/settings/profile)
```

---

## 👤 STEP 3: Developer Settings'e Git

```
1. Settings page'inde (sol sidebar)
2. Aşağı scroll et
3. "Developer settings" → Click

(Direct: https://github.com/settings/apps)
```

---

## 🔐 STEP 4: Personal Access Tokens

```
1. Developer settings sayfasında (sol sidebar)
2. "Personal access tokens" → Click
3. "Tokens (classic)" → Click

(Direct: https://github.com/settings/tokens)
```

---

## ✨ STEP 5: Yeni Token Oluştur

```
Burada göreceksiniz:
┌─────────────────────────────────┐
│ Personal access tokens          │
│                                 │
│ [Generate new token] (buton)    │
│                                 │
│ Tokens (classic)                │
│ [Generate new token (classic)]  │
└─────────────────────────────────┘

Click: "Generate new token (classic)"
```

---

## 📝 STEP 6: Token Ayarları

Açılan formda:

```
┌─────────────────────────────────────┐
│ New personal access token (classic) │
├─────────────────────────────────────┤
│                                     │
│ Token name: *                       │
│ ┌─────────────────────────────────┐ │
│ │ claude-skills-repo              │ │ ← İsim ver
│ └─────────────────────────────────┘ │
│                                     │
│ Expiration:                         │
│ [ No expiration ] ← Seç            │
│                                     │
│ Select scopes: ✓                    │
│ ☑ repo (full control) ← TİK ET     │
│ ☐ admin:repo_hook                  │
│ ☑ workflow ← TİK ET                │
│ ☐ gist                             │
│ ☐ ...                              │
│                                     │
│ [Generate token] (buton)           │
└─────────────────────────────────────┘
```

### Önemli Seçimler:

```
1. Token name: 
   "claude-skills-repo" yazınız

2. Expiration:
   "No expiration" seçiniz (expires etmesin)

3. Scopes (TİKLER):
   ☑ repo (REQUIRED)
   ☑ workflow (REQUIRED)
   
   Diğerleri untick bırakabilirsiniz.
```

---

## 🎯 STEP 7: Token Oluştur

```
"Generate token" butonuna Click
```

---

## 💾 STEP 8: Token'ı Kopyala (ÇOK ÖNEMLİ!)

```
Sonra göreceksiniz:

┌──────────────────────────────────────────┐
│ ✅ Personal access token created!        │
├──────────────────────────────────────────┤
│                                          │
│ ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx │  ← TOKEN BURADA
│ [Copy button]                            │
│                                          │
│ ⚠️  Make sure to copy your new          │
│ personal access token now. You won't    │
│ be able to see it again!                │
└──────────────────────────────────────────┘
```

### ⚠️ ÇOK ÖNEMLİ:

```
🔴 Bu token sadece BİR KEZ görünecek!
🔴 Kopyalamezseniz, tekrar oluşturman gerekir!

HEMEN KOPYALA:
1. Token'ın yanında "Copy" butonuna tıkla
2. Veya token'ı seç ve Ctrl+C (Cmd+C)
3. Bir yere (e.g., NotePad) yapıştır
```

---

## ✅ VERIFICATION

Kopyalanan token şöyle görünmeli:

```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Başlangıç: ghp_
Uzunluk: ~40 karakter
Format: Sadece harf ve sayı
```

---

## 🔓 Token Artık Hazır!

Şimdi token'ınız var! 

**Bana şunu ver:**
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 📋 KONTROL LİSTESİ

```
☐ GitHub'da giriş yaptım
☐ Settings → Developer settings → Personal access tokens
☐ "Generate new token (classic)" tıkla
☐ Name: "claude-skills-repo" (veya başka isim)
☐ Expiration: "No expiration"
☐ Scopes: ☑ repo, ☑ workflow (tıklı)
☐ "Generate token" tıkla
☐ Token kopyaladım (ghp_...)
☐ Bir yere yapıştırdım (kaydet)
```

---

## 🎉 DONE!

Token artık hazır. Bana:

```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Yazını, ben:
1. Repository klone edeceğim
2. Tüm dosyaları ekleyeceğim
3. Commit + Push yapacağım
4. PR oluşturacağım
5. Merge edeceğim

**Tüm bu işlemler 2-3 dakika içinde otomatik!** ⚡

---

## ⚠️ SEÇENEKLER (Token yoksa)

### Eğer Token yapmak istemezseniz:

**OPTION A: SSH Key (Varsa)**
```
Terminal'de:
ssh -T git@github.com

Eğer "Hi [username]!" mesajı çıkarsa,
SSH configured'dir. Bana söyle.
```

**OPTION B: Step-by-step git commands**
```
Ben adım-adım komutlar vereyim,
Siz terminal'de çalıştırın.
Tamamı 10 dakika.
```

---

## 🚀 READY?

Token'ı bana ver, ben başlayım! 

**Burada yazın:**

```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🔒 SECURITY NOTES

```
✅ SAFE:
   ☑ Token sadece push için kullanılacak
   ☑ Ben hemen after delete edeceğim
   ☑ No sensitive data exposed
   ☑ Can be revoked anytime

❌ BE CAREFUL:
   ☗ Token'ı public'te share etmeyin
   ☗ GitHub history'de exposed kalırsa revoke edin
   ☗ Token'ı save etmeyin permanent olarak
```

---

**Hazır mısınız? Token oluşturup bana gönderin!** 🔑

*GitHub Token Setup Guide - Turkish*
