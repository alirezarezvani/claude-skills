---
Name: a11y-audit
Tier: STANDARD
Category: engineering
Dependencies: none
Author: Alireza Rezvani
Version: 2.1.2
name: "a11y-audit"
description: "Accessibility audit skill for scanning, fixing, and verifying WCAG 2.2 Level A and AA compliance across React, Next.js, Vue, Angular, Svelte, and plain HTML codebases. Use when auditing accessibility, fixing a11y violations, checking color contrast, generating compliance reports, or integrating accessibility checks into CI/CD pipelines."
license: MIT
metadata:
  updated: 2026-03-18
---

# Accessibility Audit

---

**Name**: a11y-audit
**Tier**: STANDARD
**Category**: Engineering - Frontend Quality
**Dependencies**: Python 3.8+ (Standard Library Only)
**Author**: Alireza Rezvani
**Version**: 2.1.2
**Last Updated**: 2026-03-18
**License**: MIT

---

## Name

a11y-audit -- WCAG 2.2 Accessibility Audit and Remediation Skill

## Description

The a11y-audit skill provides a complete accessibility audit pipeline for modern web applications. It implements a three-phase workflow -- Scan, Fix, Verify -- that identifies WCAG 2.2 Level A and AA violations, generates exact fix code per framework, and produces stakeholder-ready compliance reports.

This skill goes beyond detection. For every violation it finds, it provides the precise before/after code fix tailored to your framework (React, Next.js, Vue, Angular, Svelte, or plain HTML). It understands that a missing `alt` attribute on an `<img>` in React JSX requires a different fix pattern than the same issue in a Vue SFC or an Angular template.

**What this skill does:**

1. **Scans** your codebase for every WCAG 2.2 Level A and AA violation, categorized by severity (Critical, Major, Minor)
2. **Fixes** each violation with framework-specific before/after code patterns
3. **Verifies** that fixes resolve the original violations and introduces no regressions
4. **Reports** findings in a structured format suitable for developers, PMs, and compliance stakeholders
5. **Integrates** into CI/CD pipelines to prevent accessibility regressions

**Key differentiators:**

- Framework-aware fix patterns (not generic HTML advice)
- Color contrast analysis with accessible alternative suggestions
- WCAG 2.2 coverage including the newest success criteria (Focus Appearance, Dragging Movements, Target Size)
- CI/CD pipeline integration with GitHub Actions, GitLab CI, and Azure DevOps
- Slash command support via `/a11y-audit`

## Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Full WCAG 2.2 Scan** | Checks all Level A and AA success criteria across your codebase |
| **Framework Detection** | Auto-detects React, Next.js, Vue, Angular, Svelte, or plain HTML |
| **Severity Classification** | Categorizes each violation as Critical, Major, or Minor |
| **Fix Code Generation** | Produces before/after code diffs for every issue |
| **Color Contrast Checker** | Validates foreground/background pairs against AA and AAA ratios |
| **Accessible Alternatives** | Suggests replacement colors that meet contrast requirements |
| **Compliance Reporting** | Generates stakeholder reports with pass/fail summaries |
| **CI/CD Integration** | GitHub Actions, GitLab CI, Azure DevOps pipeline configs |
| **Keyboard Navigation Audit** | Detects missing focus management and tab order issues |
| **ARIA Validation** | Checks for incorrect, redundant, or missing ARIA attributes |
| **Live Region Detection** | Identifies dynamic content lacking `aria-live` announcements |
| **Form Accessibility** | Validates label associations, error messaging, and input types |

### WCAG 2.2 Coverage Matrix

| Principle | Level A Criteria | Level AA Criteria |
|-----------|-----------------|-------------------|
| **Perceivable** | 1.1.1 Non-text Content, 1.2.1-1.2.3 Time-based Media, 1.3.1-1.3.3 Adaptable, 1.4.1-1.4.2 Distinguishable | 1.3.4-1.3.5 Adaptable, 1.4.3-1.4.5 Contrast & Images of Text, 1.4.10-1.4.13 Reflow & Content |
| **Operable** | 2.1.1-2.1.2 Keyboard, 2.2.1-2.2.2 Timing, 2.3.1 Seizures, 2.4.1-2.4.4 Navigable, 2.5.1-2.5.4 Input | 2.4.5-2.4.7 Navigable, 2.4.11 Focus Appearance (NEW 2.2), 2.5.7 Dragging (NEW 2.2), 2.5.8 Target Size (NEW 2.2) |
| **Understandable** | 3.1.1 Language, 3.2.1-3.2.2 Predictable, 3.3.1-3.3.2 Input Assistance | 3.1.2 Language of Parts, 3.2.3-3.2.4 Predictable, 3.3.3-3.3.4 Error Handling, 3.3.7 Redundant Entry (NEW 2.2), 3.3.8 Accessible Auth (NEW 2.2) |
| **Robust** | 4.1.2 Name/Role/Value | 4.1.3 Status Messages |

### Severity Definitions

| Severity | Definition | Example | SLA |
|----------|-----------|---------|-----|
| **Critical** | Blocks access for entire user groups | Missing alt text on informational images, no keyboard access to primary navigation | Fix before release |
| **Major** | Significant barrier that degrades experience | Insufficient color contrast on body text, missing form labels | Fix within current sprint |
| **Minor** | Usability issue that causes friction | Redundant ARIA roles, suboptimal heading hierarchy | Fix within next 2 sprints |

## Usage

### Quick Start

Activate the skill and run an audit on your project:

```bash
# Scan entire project
python scripts/a11y_scanner.py /path/to/project

# Scan with JSON output for tooling
python scripts/a11y_scanner.py /path/to/project --json

# Check color contrast for specific values
python scripts/contrast_checker.py --fg "#777777" --bg "#ffffff"

# Check contrast across a CSS/Tailwind file
python scripts/contrast_checker.py --file /path/to/styles.css
```

### Slash Command

Use the `/a11y-audit` slash command for an interactive audit session:

```
/a11y-audit                    # Audit current project
/a11y-audit --scope src/       # Audit specific directory
/a11y-audit --fix              # Audit and auto-apply fixes
/a11y-audit --report           # Generate stakeholder report
/a11y-audit --ci               # Output CI-compatible results
```

### Three-Phase Workflow

#### Phase 1: Scan

The scanner walks your source tree, detects the framework in use, and applies the appropriate rule set.

```bash
python scripts/a11y_scanner.py /path/to/project --format table
```

**Sample output:**

```
A11Y AUDIT REPORT - /path/to/project
Framework Detected: React (Next.js)
Files Scanned: 127
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CRITICAL (3 issues)
  [1.1.1] src/components/Hero.tsx:14
    Missing alt text on <img> element
  [2.1.1] src/components/Modal.tsx:8
    Focus not trapped inside modal dialog
  [1.4.3] src/styles/globals.css:42
    Contrast ratio 2.8:1 on .subtitle (requires 4.5:1)

MAJOR (7 issues)
  [2.4.11] src/components/Button.tsx:22
    Focus indicator not visible (2px outline required)
  [1.3.1] src/components/Form.tsx:31
    Input missing associated <label>
  ...

MINOR (4 issues)
  [1.3.1] src/components/Nav.tsx:5
    <nav> has redundant role="navigation"
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY: 14 violations (3 Critical, 7 Major, 4 Minor)
WCAG 2.2 Level A:  8 issues
WCAG 2.2 Level AA: 6 issues
```

#### Phase 2: Fix

For each violation, apply the framework-specific fix. The skill provides exact before/after code for every issue type.

See the [Fix Patterns by Framework](#fix-patterns-by-framework) section below for the complete fix catalog.

#### Phase 3: Verify

Re-run the scanner to confirm all fixes are applied and no regressions were introduced:

```bash
# Re-scan after fixes
python scripts/a11y_scanner.py /path/to/project --format table

# Compare against baseline
python scripts/a11y_scanner.py /path/to/project --baseline audit-baseline.json
```

**Verification output:**

```
VERIFICATION RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Previous Scan:  14 violations (3 Critical, 7 Major, 4 Minor)
Current Scan:    2 violations (0 Critical, 1 Major, 1 Minor)
Resolved:       12 violations
New Issues:      0 regressions

STATUS: IMPROVED (85.7% reduction)
```

## Examples

### Example 1: React Component Audit

Given a React component with multiple accessibility issues:

```tsx
// BEFORE: src/components/ProductCard.tsx
function ProductCard({ product }) {
  return (
    <div onClick={() => navigate(`/product/${product.id}`)}>
      <img src={product.image} />
      <div style={{ color: '#aaa', fontSize: '12px' }}>
        {product.name}
      </div>
      <span style={{ color: '#999' }}>${product.price}</span>
    </div>
  );
}
```

**Violations detected:**

| # | WCAG | Severity | Issue |
|---|------|----------|-------|
| 1 | 1.1.1 | Critical | `<img>` missing `alt` attribute |
| 2 | 2.1.1 | Critical | `<div onClick>` not keyboard accessible |
| 3 | 1.4.3 | Major | Color `#aaa` on white fails contrast (2.32:1, needs 4.5:1) |
| 4 | 1.4.3 | Major | Color `#999` on white fails contrast (2.85:1, needs 4.5:1) |
| 5 | 4.1.2 | Major | Interactive element missing role and accessible name |

```tsx
// AFTER: src/components/ProductCard.tsx
function ProductCard({ product }) {
  return (
    <a
      href={`/product/${product.id}`}
      className="product-card"
      aria-label={`View ${product.name} - $${product.price}`}
    >
      <img src={product.image} alt={product.imageAlt || product.name} />
      <div style={{ color: '#595959', fontSize: '12px' }}>
        {product.name}
      </div>
      <span style={{ color: '#767676' }}>${product.price}</span>
    </a>
  );
}
```

**What changed:**
- `<div onClick>` replaced with `<a href>` for native keyboard and screen reader support
- `alt` attribute added to `<img>` with meaningful fallback
- `aria-label` provides full context for assistive technology
- Color `#aaa` replaced with `#595959` (7.01:1 contrast ratio -- passes AA and AAA)
- Color `#999` replaced with `#767676` (4.54:1 contrast ratio -- passes AA)

### Example 2: Vue SFC Form Audit

```vue
<!-- BEFORE: src/components/LoginForm.vue -->
<template>
  <form @submit="handleLogin">
    <input type="text" placeholder="Email" v-model="email" />
    <input type="password" placeholder="Password" v-model="password" />
    <div v-if="error" style="color: red">{{ error }}</div>
    <div @click="handleLogin">Sign In</div>
  </form>
</template>
```

**Violations detected:**

| # | WCAG | Severity | Issue |
|---|------|----------|-------|
| 1 | 1.3.1 | Critical | Inputs missing associated `<label>` elements |
| 2 | 3.3.2 | Major | Placeholder text used as only label (disappears on input) |
| 3 | 2.1.1 | Critical | `<div @click>` not keyboard accessible |
| 4 | 4.1.3 | Major | Error message not announced to screen readers |
| 5 | 3.3.1 | Major | Error not programmatically associated with input |

```vue
<!-- AFTER: src/components/LoginForm.vue -->
<template>
  <form @submit.prevent="handleLogin" aria-label="Sign in to your account">
    <div class="field">
      <label for="login-email">Email</label>
      <input
        id="login-email"
        type="email"
        v-model="email"
        autocomplete="email"
        required
        :aria-describedby="emailError ? 'email-error' : undefined"
        :aria-invalid="!!emailError"
      />
      <span v-if="emailError" id="email-error" role="alert">
        {{ emailError }}
      </span>
    </div>
    <div class="field">
      <label for="login-password">Password</label>
      <input
        id="login-password"
        type="password"
        v-model="password"
        autocomplete="current-password"
        required
        :aria-describedby="passwordError ? 'password-error' : undefined"
        :aria-invalid="!!passwordError"
      />
      <span v-if="passwordError" id="password-error" role="alert">
        {{ passwordError }}
      </span>
    </div>
    <div v-if="error" role="alert" aria-live="assertive" class="form-error">
      {{ error }}
    </div>
    <button type="submit">Sign In</button>
  </form>
</template>
```

### Example 3: Angular Template Audit

```html
<!-- BEFORE: src/app/dashboard/dashboard.component.html -->
<div class="tabs">
  <div *ngFor="let tab of tabs"
       (click)="selectTab(tab)"
       [class.active]="tab.active">
    {{ tab.label }}
  </div>
</div>
<div class="tab-content">
  <div *ngIf="selectedTab">{{ selectedTab.content }}</div>
</div>
```

**Violations detected:**

| # | WCAG | Severity | Issue |
|---|------|----------|-------|
| 1 | 4.1.2 | Critical | Tab widget missing ARIA roles (`tablist`, `tab`, `tabpanel`) |
| 2 | 2.1.1 | Critical | Tabs not keyboard navigable (arrow keys, Home, End) |
| 3 | 2.4.11 | Major | No visible focus indicator on active tab |

```html
<!-- AFTER: src/app/dashboard/dashboard.component.html -->
<div class="tabs" role="tablist" aria-label="Dashboard sections">
  <button
    *ngFor="let tab of tabs; let i = index"
    role="tab"
    [id]="'tab-' + tab.id"
    [attr.aria-selected]="tab.active"
    [attr.aria-controls]="'panel-' + tab.id"
    [attr.tabindex]="tab.active ? 0 : -1"
    (click)="selectTab(tab)"
    (keydown)="handleTabKeydown($event, i)"
    class="tab-button"
    [class.active]="tab.active">
    {{ tab.label }}
  </button>
</div>
<div
  *ngIf="selectedTab"
  role="tabpanel"
  [id]="'panel-' + selectedTab.id"
  [attr.aria-labelledby]="'tab-' + selectedTab.id"
  tabindex="0"
  class="tab-content">
  {{ selectedTab.content }}
</div>
```

**Supporting TypeScript for keyboard navigation:**

```typescript
// dashboard.component.ts
handleTabKeydown(event: KeyboardEvent, index: number): void {
  const tabCount = this.tabs.length;
  let newIndex = index;

  switch (event.key) {
    case 'ArrowRight':
      newIndex = (index + 1) % tabCount;
      break;
    case 'ArrowLeft':
      newIndex = (index - 1 + tabCount) % tabCount;
      break;
    case 'Home':
      newIndex = 0;
      break;
    case 'End':
      newIndex = tabCount - 1;
      break;
    default:
      return;
  }

  event.preventDefault();
  this.selectTab(this.tabs[newIndex]);
  // Move focus to the new tab button
  const tabElement = document.getElementById(`tab-${this.tabs[newIndex].id}`);
  tabElement?.focus();
}
```

### Example 4: Next.js Page-Level Audit

```tsx
// BEFORE: src/app/page.tsx
export default function Home() {
  return (
    <main>
      <div className="text-4xl font-bold">Welcome to Acme</div>
      <div className="mt-4">
        Build better products with our platform.
      </div>
      <div className="mt-8 bg-blue-600 text-white px-6 py-3 rounded cursor-pointer"
           onClick={() => router.push('/signup')}>
        Get Started
      </div>
    </main>
  );
}
```

**Violations detected:**

| # | WCAG | Severity | Issue |
|---|------|----------|-------|
| 1 | 1.3.1 | Major | Heading uses `<div>` instead of `<h1>` -- no semantic structure |
| 2 | 2.4.2 | Major | Page missing `<title>` (Next.js metadata) |
| 3 | 2.1.1 | Critical | CTA uses `<div onClick>` -- not keyboard accessible |
| 4 | 3.1.1 | Minor | `<html>` missing `lang` attribute (check `layout.tsx`) |

```tsx
// AFTER: src/app/page.tsx
import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Acme - Build Better Products',
  description: 'Build better products with the Acme platform.',
};

export default function Home() {
  return (
    <main>
      <h1 className="text-4xl font-bold">Welcome to Acme</h1>
      <p className="mt-4">
        Build better products with our platform.
      </p>
      <Link
        href="/signup"
        className="mt-8 inline-block bg-blue-600 text-white px-6 py-3 rounded
                   hover:bg-blue-700 focus-visible:outline focus-visible:outline-2
                   focus-visible:outline-offset-2 focus-visible:outline-blue-600"
      >
        Get Started
      </Link>
    </main>
  );
}
```

```tsx
// Also fix: src/app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

### Example 5: Svelte Component Audit

```svelte
<!-- BEFORE: src/lib/components/Accordion.svelte -->
<script>
  let openIndex = -1;
  function toggle(i) { openIndex = openIndex === i ? -1 : i; }
</script>

{#each items as item, i}
  <div class="header" on:click={() => toggle(i)}>
    {item.title}
  </div>
  {#if openIndex === i}
    <div class="content">{item.body}</div>
  {/if}
{/each}
```

**Violations detected:**

| # | WCAG | Severity | Issue |
|---|------|----------|-------|
| 1 | 4.1.2 | Critical | Accordion missing ARIA roles and properties |
| 2 | 2.1.1 | Critical | Headers not keyboard accessible |
| 3 | 2.5.8 | Minor | Click targets may be smaller than 24x24px (NEW in WCAG 2.2) |

```svelte
<!-- AFTER: src/lib/components/Accordion.svelte -->
<script>
  export let items = [];
  let openIndex = -1;

  function toggle(i) {
    openIndex = openIndex === i ? -1 : i;
  }

  function handleKeydown(event, i) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      toggle(i);
    }
  }
</script>

<div class="accordion">
  {#each items as item, i}
    <h3>
      <button
        class="accordion-header"
        aria-expanded={openIndex === i}
        aria-controls="panel-{i}"
        id="header-{i}"
        on:click={() => toggle(i)}
        on:keydown={(e) => handleKeydown(e, i)}
      >
        {item.title}
        <span class="icon" aria-hidden="true">
          {openIndex === i ? '−' : '+'}
        </span>
      </button>
    </h3>
    <div
      id="panel-{i}"
      role="region"
      aria-labelledby="header-{i}"
      class="accordion-content"
      class:open={openIndex === i}
      hidden={openIndex !== i}
    >
      {item.body}
    </div>
  {/each}
</div>

<style>
  .accordion-header {
    min-height: 44px; /* WCAG 2.5.8 Target Size */
    width: 100%;
    padding: 12px 16px;
    cursor: pointer;
    text-align: left;
  }
  .accordion-header:focus-visible {
    outline: 2px solid #005fcc;
    outline-offset: 2px;
  }
</style>
```

## Fix Patterns by Framework

### React / Next.js Fix Patterns

#### Missing Alt Text (1.1.1)

```tsx
// BEFORE
<img src={hero} />

// AFTER - Informational image
<img src={hero} alt="Team collaborating around a whiteboard" />

// AFTER - Decorative image
<img src={divider} alt="" role="presentation" />
```

#### Non-Interactive Element with Click Handler (2.1.1)

```tsx
// BEFORE
<div onClick={handleClick}>Click me</div>

// AFTER - If it navigates
<Link href="/destination">Click me</Link>

// AFTER - If it performs an action
<button type="button" onClick={handleClick}>Click me</button>
```

#### Missing Focus Management in Modals (2.4.3)

```tsx
// BEFORE
function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null;
  return <div className="modal-overlay">{children}</div>;
}

// AFTER
import { useEffect, useRef } from 'react';

function Modal({ isOpen, onClose, children, title }) {
  const modalRef = useRef(null);
  const previousFocus = useRef(null);

  useEffect(() => {
    if (isOpen) {
      previousFocus.current = document.activeElement;
      modalRef.current?.focus();
    } else {
      previousFocus.current?.focus();
    }
  }, [isOpen]);

  useEffect(() => {
    if (!isOpen) return;
    const handleKeydown = (e) => {
      if (e.key === 'Escape') onClose();
      if (e.key === 'Tab') {
        const focusable = modalRef.current?.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (!focusable?.length) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    };
    document.addEventListener('keydown', handleKeydown);
    return () => document.removeEventListener('keydown', handleKeydown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose} aria-hidden="true">
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-label={title}
        tabIndex={-1}
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          aria-label="Close dialog"
          className="modal-close"
        >
          &times;
        </button>
        {children}
      </div>
    </div>
  );
}
```

#### Focus Appearance (2.4.11 -- NEW in WCAG 2.2)

```css
/* BEFORE */
button:focus {
  outline: none; /* Removes default focus indicator */
}

/* AFTER - Meets WCAG 2.2 Focus Appearance */
button:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}
```

```tsx
// Tailwind CSS pattern
<button className="focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600">
  Submit
</button>
```

### Vue Fix Patterns

#### Missing Form Labels (1.3.1)

```vue
<!-- BEFORE -->
<input type="text" v-model="name" placeholder="Name" />

<!-- AFTER -->
<label for="user-name">Name</label>
<input id="user-name" type="text" v-model="name" autocomplete="name" />
```

#### Dynamic Content Without Live Region (4.1.3)

```vue
<!-- BEFORE -->
<div v-if="status">{{ statusMessage }}</div>

<!-- AFTER -->
<div aria-live="polite" aria-atomic="true">
  <p v-if="status">{{ statusMessage }}</p>
</div>
```

#### Vue Router Navigation Announcements (2.4.2)

```typescript
// router/index.ts
router.afterEach((to) => {
  const title = to.meta.title || 'Page';
  document.title = `${title} | My App`;

  // Announce route change to screen readers
  const announcer = document.getElementById('route-announcer');
  if (announcer) {
    announcer.textContent = `Navigated to ${title}`;
  }
});
```

```vue
<!-- App.vue - Add announcer element -->
<div
  id="route-announcer"
  role="status"
  aria-live="assertive"
  aria-atomic="true"
  class="sr-only"
></div>
```

### Angular Fix Patterns

#### Missing ARIA on Custom Components (4.1.2)

```typescript
// BEFORE
@Component({
  selector: 'app-dropdown',
  template: `
    <div (click)="toggle()">{{ selected }}</div>
    <div *ngIf="isOpen">
      <div *ngFor="let opt of options" (click)="select(opt)">{{ opt }}</div>
    </div>
  `
})

// AFTER
@Component({
  selector: 'app-dropdown',
  template: `
    <button
      role="combobox"
      [attr.aria-expanded]="isOpen"
      aria-haspopup="listbox"
      [attr.aria-label]="label"
      (click)="toggle()"
      (keydown)="handleKeydown($event)"
    >
      {{ selected }}
    </button>
    <ul *ngIf="isOpen" role="listbox" [attr.aria-label]="label + ' options'">
      <li
        *ngFor="let opt of options; let i = index"
        role="option"
        [attr.aria-selected]="opt === selected"
        [attr.id]="'option-' + i"
        (click)="select(opt)"
        (keydown)="handleOptionKeydown($event, opt, i)"
        tabindex="-1"
      >
        {{ opt }}
      </li>
    </ul>
  `
})
```

#### Angular CDK A11y Module Integration

```typescript
// Use Angular CDK for focus trap in dialogs
import { A11yModule } from '@angular/cdk/a11y';

@Component({
  template: `
    <div cdkTrapFocus cdkTrapFocusAutoCapture>
      <h2 id="dialog-title">Edit Profile</h2>
      <!-- dialog content -->
    </div>
  `
})
```

### Svelte Fix Patterns

#### Accessible Announcements (4.1.3)

```svelte
<!-- BEFORE -->
{#if message}
  <p class="toast">{message}</p>
{/if}

<!-- AFTER -->
<div aria-live="polite" class="sr-only">
  {#if message}
    <p>{message}</p>
  {/if}
</div>
<div class="toast" aria-hidden="true">
  {#if message}
    <p>{message}</p>
  {/if}
</div>
```

#### SvelteKit Page Titles (2.4.2)

```svelte
<!-- +page.svelte -->
<svelte:head>
  <title>Dashboard | My App</title>
</svelte:head>
```

### Plain HTML Fix Patterns

#### Skip Navigation Link (2.4.1)

```html
<!-- BEFORE -->
<body>
  <nav><!-- long navigation --></nav>
  <main><!-- content --></main>
</body>

<!-- AFTER -->
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <nav aria-label="Main navigation"><!-- long navigation --></nav>
  <main id="main-content" tabindex="-1"><!-- content --></main>
</body>
```

```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  padding: 8px 16px;
  background: #005fcc;
  color: #fff;
  z-index: 1000;
  transition: top 0.2s;
}
.skip-link:focus {
  top: 0;
}
```

#### Accessible Data Table (1.3.1)

```html
<!-- BEFORE -->
<table>
  <tr><td>Name</td><td>Email</td><td>Role</td></tr>
  <tr><td>Alice</td><td>alice@co.com</td><td>Admin</td></tr>
</table>

<!-- AFTER -->
<table aria-label="Team members">
  <caption class="sr-only">List of team members and their roles</caption>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Email</th>
      <th scope="col">Role</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Alice</th>
      <td>alice@co.com</td>
      <td>Admin</td>
    </tr>
  </tbody>
</table>
```

## Color Contrast Checker

The `contrast_checker.py` script validates color pairs against WCAG 2.2 contrast requirements.

### Usage

```bash
# Check a single color pair
python scripts/contrast_checker.py --fg "#777777" --bg "#ffffff"

# Output:
# Foreground: #777777 | Background: #ffffff
# Contrast Ratio: 4.48:1
# AA Normal Text (4.5:1): FAIL
# AA Large Text (3.0:1):  PASS
# AAA Normal Text (7.0:1): FAIL
# Suggested alternative: #767676 (4.54:1 - passes AA)

# Scan a CSS file for all color pairs
python scripts/contrast_checker.py --file src/styles/globals.css

# Scan Tailwind classes in components
python scripts/contrast_checker.py --tailwind src/components/
```

### Common Contrast Fixes

| Original Color | Contrast on White | Fix | New Contrast |
|----------------|------------------|-----|--------------|
| `#aaaaaa` | 2.32:1 | `#767676` | 4.54:1 (AA) |
| `#999999` | 2.85:1 | `#767676` | 4.54:1 (AA) |
| `#888888` | 3.54:1 | `#767676` | 4.54:1 (AA) |
| `#777777` | 4.48:1 | `#757575` | 4.60:1 (AA) |
| `#66bb6a` | 3.06:1 | `#2e7d32` | 5.87:1 (AA) |
| `#42a5f5` | 2.81:1 | `#1565c0` | 6.08:1 (AA) |
| `#ef5350` | 3.13:1 | `#c62828` | 5.57:1 (AA) |

### Tailwind CSS Accessible Palette Mapping

| Inaccessible Class | Contrast on White | Accessible Alternative | Contrast |
|---------------------|------------------|----------------------|----------|
| `text-gray-400` | 2.68:1 | `text-gray-600` | 5.74:1 |
| `text-blue-400` | 2.81:1 | `text-blue-700` | 5.96:1 |
| `text-green-400` | 2.12:1 | `text-green-700` | 5.18:1 |
| `text-red-400` | 3.04:1 | `text-red-700` | 6.05:1 |
| `text-yellow-500` | 1.47:1 | `text-yellow-800` | 7.34:1 |

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/a11y-audit.yml
name: Accessibility Audit

on:
  pull_request:
    paths:
      - 'src/**/*.tsx'
      - 'src/**/*.vue'
      - 'src/**/*.html'
      - 'src/**/*.svelte'

jobs:
  a11y-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run A11y Scanner
        run: |
          python scripts/a11y_scanner.py ./src --json > a11y-results.json

      - name: Check for Critical Issues
        run: |
          python -c "
          import json, sys
          with open('a11y-results.json') as f:
              data = json.load(f)
          critical = [v for v in data.get('violations', []) if v['severity'] == 'critical']
          if critical:
              print(f'FAILED: {len(critical)} critical a11y violations found')
              for v in critical:
                  print(f\"  [{v['wcag']}] {v['file']}:{v['line']} - {v['message']}\")
              sys.exit(1)
          print('PASSED: No critical a11y violations')
          "

      - name: Upload Audit Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: a11y-audit-report
          path: a11y-results.json

      - name: Comment on PR
        if: failure()
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          header: a11y-audit
          message: |
            ## Accessibility Audit Failed
            Critical WCAG 2.2 violations were found. See the uploaded artifact for details.
            Run `python scripts/a11y_scanner.py ./src` locally to view and fix issues.
```

### GitLab CI

```yaml
# .gitlab-ci.yml
a11y-audit:
  stage: test
  image: python:3.11-slim
  script:
    - python scripts/a11y_scanner.py ./src --json > a11y-results.json
    - python -c "
      import json, sys;
      data = json.load(open('a11y-results.json'));
      critical = [v for v in data.get('violations', []) if v['severity'] == 'critical'];
      sys.exit(1) if critical else print('A11y audit passed')
      "
  artifacts:
    paths:
      - a11y-results.json
    when: always
  rules:
    - changes:
        - "src/**/*.{tsx,vue,html,svelte}"
```

### Azure DevOps

```yaml
# azure-pipelines.yml
- task: PythonScript@0
  displayName: 'Run A11y Audit'
  inputs:
    scriptSource: 'filePath'
    scriptPath: 'scripts/a11y_scanner.py'
    arguments: './src --json --output $(Build.ArtifactStagingDirectory)/a11y-results.json'

- task: PublishBuildArtifacts@1
  condition: always()
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)/a11y-results.json'
    ArtifactName: 'a11y-audit-report'
```

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run a11y scan on staged files only
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(tsx|vue|html|svelte|jsx)$')

if [ -n "$STAGED_FILES" ]; then
  echo "Running accessibility audit on staged files..."
  for file in $STAGED_FILES; do
    python scripts/a11y_scanner.py "$file" --severity critical --quiet
    if [ $? -ne 0 ]; then
      echo "A11y audit FAILED for $file. Fix critical issues before committing."
      exit 1
    fi
  done
  echo "A11y audit passed."
fi
```

## Common Pitfalls

| Pitfall | Why It Happens | Correct Approach |
|---------|---------------|------------------|
| Using `role="button"` on a `<div>` | Developers think ARIA makes any element interactive | Use a native `<button>` element instead -- it includes keyboard handling, focus, and click events for free |
| Setting `tabindex="0"` on everything | Attempting to make elements focusable | Only interactive elements need focus. Use native elements (`<a>`, `<button>`, `<input>`) which are focusable by default |
| Using `aria-label` on non-interactive elements | Trying to add descriptions to `<div>` or `<span>` | Screen readers may ignore `aria-label` on generic elements. Use `aria-labelledby` pointing to visible text, or restructure with headings |
| Hiding content with `display: none` for screen readers | Wanting visual hiding | `display: none` hides from ALL users, including screen readers. Use `.sr-only` class for screen-reader-only content |
| Using color alone to convey meaning | Red/green for status, error states | Add icons, text labels, or patterns alongside color. WCAG 1.4.1 requires non-color indicators |
| Placeholder text as the only label | Saves visual space | Placeholder disappears on input, fails 1.3.1 and 3.3.2. Always provide a visible `<label>` |
| Auto-playing video or audio | Engagement metrics | Violates 1.4.2. Never autoplay media with sound. Provide pause/stop controls |
| `outline: none` without replacement | Design preference | Violates 2.4.7 and 2.4.11. Always provide a visible focus indicator, use `focus-visible` to limit to keyboard users |
| Empty `alt=""` on informational images | Misunderstanding empty alt | Empty alt marks images as decorative. Informational images need descriptive alt text |
| Missing heading hierarchy (h1 -> h3, skipping h2) | Visual styling drives heading choice | Heading levels must be sequential. Use CSS for styling, HTML for structure |
| `onClick` without `onKeyDown` on custom elements | Mouse-first development | Custom interactive elements need keyboard support. Prefer native elements or add `onKeyDown` with Enter/Space handling |
| Inaccessible custom `<select>` replacements | Design requirements override native controls | Custom dropdowns need full ARIA: `combobox`, `listbox`, `option` roles, plus keyboard navigation (arrows, type-ahead, Escape) |
| Ignoring `prefers-reduced-motion` | Animations assumed safe for all | Wrap animations in `@media (prefers-reduced-motion: no-preference)` or provide reduced alternatives |
| CAPTCHAs without alternatives | Bot prevention | Violates 3.3.8 (WCAG 2.2). Provide alternative verification methods (email, SMS) alongside visual CAPTCHAs |

## Screen Reader Utility Class

Every project should include this utility class for visually hiding content while keeping it accessible to screen readers:

```css
/* Visually hidden but accessible to screen readers */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Allow the element to be focusable when navigated to via keyboard */
.sr-only-focusable:focus,
.sr-only-focusable:active {
  position: static;
  width: auto;
  height: auto;
  padding: inherit;
  margin: inherit;
  overflow: visible;
  clip: auto;
  white-space: inherit;
}
```

Tailwind CSS includes this as `sr-only` by default. For other frameworks:
- **Angular**: Add to `styles.scss`
- **Vue**: Add to `assets/global.css`
- **Svelte**: Add to `app.css`

## Audit Report Template

The scanner generates a stakeholder-ready report when run with the `--report` flag:

```bash
python scripts/a11y_scanner.py /path/to/project --report --output audit-report.md
```

**Generated report structure:**

```markdown
# Accessibility Audit Report
**Project:** Acme Dashboard
**Date:** 2026-03-18
**Standard:** WCAG 2.2 Level AA
**Tool:** a11y-audit v2.1.2

## Executive Summary
- Files Scanned: 127
- Total Violations: 14
- Critical: 3 | Major: 7 | Minor: 4
- Estimated Remediation: 8-12 hours
- Compliance Score: 72% (Target: 100%)

## Violations by Category
| Category | Count | Severity Breakdown |
|----------|-------|--------------------|
| Missing Alt Text | 3 | 2 Critical, 1 Minor |
| Keyboard Access | 4 | 2 Critical, 2 Major |
| Color Contrast | 3 | 3 Major |
| Form Labels | 2 | 2 Major |
| ARIA Usage | 2 | 2 Minor |

## Detailed Findings
[Per-violation details with file, line, WCAG criterion, and fix]

## Remediation Priority
1. Fix all Critical issues (blocks release)
2. Fix Major issues in current sprint
3. Schedule Minor issues for next sprint

## Recommendations
- Add a11y linting to CI pipeline (eslint-plugin-jsx-a11y)
- Include keyboard testing in QA checklist
- Schedule quarterly manual audit with assistive technology
```

## Tools Reference

### a11y_scanner.py

Scans source files for WCAG 2.2 violations.

```
Usage: python scripts/a11y_scanner.py <path> [options]

Arguments:
  path                    File or directory to scan

Options:
  --json                  Output results as JSON
  --format {table,csv}    Output format (default: table)
  --severity {critical,major,minor}
                          Filter by minimum severity
  --framework {react,vue,angular,svelte,html,auto}
                          Force framework (default: auto-detect)
  --baseline FILE         Compare against previous scan results
  --report                Generate stakeholder report
  --output FILE           Write results to file
  --quiet                 Suppress output, exit code only
  --ci                    CI mode: non-zero exit on critical issues
```

### contrast_checker.py

Validates color contrast ratios against WCAG 2.2 requirements.

```
Usage: python scripts/contrast_checker.py [options]

Options:
  --fg COLOR              Foreground color (hex)
  --bg COLOR              Background color (hex)
  --file FILE             Scan CSS file for color pairs
  --tailwind DIR          Scan directory for Tailwind color classes
  --json                  Output results as JSON
  --suggest               Suggest accessible alternatives for failures
  --level {aa,aaa}        Target conformance level (default: aa)
```

## Testing Checklist

Use this checklist after applying fixes to verify accessibility manually:

### Keyboard Navigation
- [ ] All interactive elements reachable via Tab key
- [ ] Tab order follows visual/logical reading order
- [ ] Focus indicator visible on every focusable element (2px+ outline)
- [ ] Modals trap focus and return focus on close
- [ ] Escape key closes modals, dropdowns, and popups
- [ ] Arrow keys navigate within composite widgets (tabs, menus, listboxes)
- [ ] No keyboard traps (user can always Tab away)

### Screen Reader
- [ ] All images have appropriate alt text (or `alt=""` for decorative)
- [ ] Headings create logical document outline (h1 -> h2 -> h3)
- [ ] Form inputs have associated labels
- [ ] Error messages announced via `aria-live` or `role="alert"`
- [ ] Page title updates on navigation (SPA)
- [ ] Dynamic content changes announced appropriately

### Visual
- [ ] Text contrast meets 4.5:1 for normal text, 3:1 for large text
- [ ] UI component contrast meets 3:1 against background
- [ ] Content reflows without horizontal scrolling at 320px width
- [ ] Text resizable to 200% without loss of content
- [ ] No information conveyed by color alone
- [ ] Focus indicators meet 2.4.11 Focus Appearance criteria

### Motion and Media
- [ ] Animations respect `prefers-reduced-motion`
- [ ] No auto-playing media with audio
- [ ] No content flashing more than 3 times per second
- [ ] Video has captions; audio has transcripts

### Forms
- [ ] All inputs have visible labels
- [ ] Required fields indicated (not by color alone)
- [ ] Error messages specific and associated with input via `aria-describedby`
- [ ] Autocomplete attributes present on common fields (name, email, etc.)
- [ ] No CAPTCHA without alternative method (WCAG 2.2 3.3.8)

## WCAG 2.2 New Success Criteria Reference

These criteria were added in WCAG 2.2 and are commonly missed:

### 2.4.11 Focus Appearance (Level AA)

The focus indicator must have a minimum area of a 2px perimeter around the component and a contrast ratio of at least 3:1 against adjacent colors.

**Pattern:**
```css
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}
```

### 2.5.7 Dragging Movements (Level AA)

Any functionality that uses dragging must have a single-pointer alternative (click, tap).

**Pattern:**
```tsx
// Sortable list: support both drag and button-based reorder
<li draggable onDragStart={handleDrag}>
  {item.name}
  <button onClick={() => moveUp(index)} aria-label={`Move ${item.name} up`}>
    Move Up
  </button>
  <button onClick={() => moveDown(index)} aria-label={`Move ${item.name} down`}>
    Move Down
  </button>
</li>
```

### 2.5.8 Target Size (Level AA)

Interactive targets must be at least 24x24 CSS pixels, with exceptions for inline text links and elements where the spacing provides equivalent clearance.

**Pattern:**
```css
button, a, input, select, textarea {
  min-height: 24px;
  min-width: 24px;
}

/* Recommended: 44x44px for touch targets */
@media (pointer: coarse) {
  button, a, input[type="checkbox"], input[type="radio"] {
    min-height: 44px;
    min-width: 44px;
  }
}
```

### 3.3.7 Redundant Entry (Level A)

Information previously entered by the user must be auto-populated or available for selection when needed again in the same process.

**Pattern:**
```tsx
// Multi-step form: persist data across steps
const [formData, setFormData] = useState({});

// Step 2 pre-fills shipping address from billing
<input
  defaultValue={formData.billingAddress || ''}
  autoComplete="shipping street-address"
/>
```

### 3.3.8 Accessible Authentication (Level AA)

Authentication must not require cognitive function tests (e.g., remembering a password, solving a puzzle) unless an alternative is provided.

**Pattern:**
- Support password managers (`autocomplete="current-password"`)
- Offer passkey / biometric authentication
- Allow copy-paste in password fields (never block paste)
- Provide email/SMS OTP as alternative to CAPTCHA

## Related Skills

| Skill | Relationship | Path |
|-------|-------------|------|
| **senior-frontend** | Frontend patterns used in a11y fixes (React, Next.js, Tailwind) | `engineering-team/senior-frontend/` |
| **code-reviewer** | Include a11y checks in code review workflows | `engineering-team/code-reviewer/` |
| **senior-qa** | Integration of a11y testing into QA processes | `engineering-team/senior-qa/` |
| **playwright-pro** | Automated browser testing with accessibility assertions | `engineering-team/playwright-pro/` |
| **senior-secops** | Accessibility as part of compliance and security posture | `engineering-team/senior-secops/` |
| **epic-design** | WCAG 2.1 AA compliant animations and scroll storytelling | `engineering-team/epic-design/` |
| **tdd-guide** | Test-driven development patterns for a11y test cases | `engineering-team/tdd-guide/` |
| **incident-commander** | Respond to a11y compliance incidents and legal risk | `engineering-team/incident-commander/` |

## Resources

- [WCAG 2.2 Specification](https://www.w3.org/TR/WCAG22/)
- [WAI-ARIA Authoring Practices 1.2](https://www.w3.org/WAI/ARIA/apg/)
- [Deque axe-core Rules](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)
- [eslint-plugin-jsx-a11y](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y)
- [vue-a11y](https://vue-a11y.com/)
- [@angular-eslint/template-accessibility](https://github.com/angular-eslint/angular-eslint)

---

**License:** MIT
**Author:** Alireza Rezvani
**Version:** 2.1.2
