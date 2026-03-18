# Framework-Specific Accessibility Patterns

## React / Next.js

### Common Issues and Fixes

**Image alt text:**
```jsx
// ❌ Bad
<img src="/hero.jpg" />
<Image src="/hero.jpg" width={800} height={400} />

// ✅ Good
<img src="/hero.jpg" alt="Team collaborating in office" />
<Image src="/hero.jpg" width={800} height={400} alt="Team collaborating in office" />

// ✅ Decorative image
<img src="/divider.svg" alt="" role="presentation" />
```

**Form labels:**
```jsx
// ❌ Bad — placeholder as label
<input placeholder="Email" type="email" />

// ✅ Good — explicit label
<label htmlFor="email">Email</label>
<input id="email" type="email" placeholder="user@example.com" />

// ✅ Good — aria-label for icon-only inputs
<input type="search" aria-label="Search products" />
```

**Click handlers on divs:**
```jsx
// ❌ Bad — not keyboard accessible
<div onClick={handleClick}>Click me</div>

// ✅ Good — use button
<button onClick={handleClick}>Click me</button>

// ✅ If div is required — add keyboard support
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') handleClick(); }}
>
  Click me
</div>
```

**SPA route announcements (Next.js App Router):**
```jsx
// Layout component — announce page changes
'use client';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';

export function RouteAnnouncer() {
  const pathname = usePathname();
  const [announcement, setAnnouncement] = useState('');

  useEffect(() => {
    const title = document.title;
    setAnnouncement(`Navigated to ${title}`);
  }, [pathname]);

  return (
    <div aria-live="assertive" role="status" className="sr-only">
      {announcement}
    </div>
  );
}
```

**Focus management after dynamic content:**
```jsx
// After adding item to list, announce it
const [items, setItems] = useState([]);
const statusRef = useRef(null);

const addItem = (item) => {
  setItems([...items, item]);
  // Announce to screen readers
  statusRef.current.textContent = `${item.name} added to list`;
};

return (
  <>
    <div ref={statusRef} aria-live="polite" className="sr-only" />
    {/* list content */}
  </>
);
```

### React-Specific Libraries
- `@radix-ui/*` — accessible primitives (Dialog, Tabs, Select, etc.)
- `@headlessui/react` — unstyled accessible components
- `react-aria` — Adobe's accessibility hooks
- `eslint-plugin-jsx-a11y` — lint rules for JSX accessibility

## Vue 3

### Common Issues and Fixes

**Dynamic content announcements:**
```vue
<template>
  <div aria-live="polite" class="sr-only">
    {{ announcement }}
  </div>
  <button @click="search">Search</button>
  <ul v-if="results.length">
    <li v-for="r in results" :key="r.id">{{ r.name }}</li>
  </ul>
</template>

<script setup>
import { ref } from 'vue';
const results = ref([]);
const announcement = ref('');

async function search() {
  results.value = await fetchResults();
  announcement.value = `${results.value.length} results found`;
}
</script>
```

**Conditional rendering with focus:**
```vue
<template>
  <button @click="showForm = true">Add Item</button>
  <form v-if="showForm" ref="formRef">
    <label for="name">Name</label>
    <input id="name" ref="nameInput" />
  </form>
</template>

<script setup>
import { ref, nextTick } from 'vue';
const showForm = ref(false);
const nameInput = ref(null);

watch(showForm, async (val) => {
  if (val) {
    await nextTick();
    nameInput.value?.focus();
  }
});
</script>
```

### Vue-Specific Libraries
- `vue-announcer` — route change announcements
- `@headlessui/vue` — accessible components
- `eslint-plugin-vuejs-accessibility` — lint rules

## Angular

### Common Issues and Fixes

**CDK accessibility utilities:**
```typescript
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { FocusTrapFactory } from '@angular/cdk/a11y';

@Component({...})
export class MyComponent {
  constructor(
    private liveAnnouncer: LiveAnnouncer,
    private focusTrapFactory: FocusTrapFactory
  ) {}

  addItem(item: Item) {
    this.items.push(item);
    this.liveAnnouncer.announce(`${item.name} added`);
  }

  openDialog(element: HTMLElement) {
    const focusTrap = this.focusTrapFactory.create(element);
    focusTrap.focusInitialElement();
  }
}
```

**Template-driven forms:**
```html
<!-- ❌ Bad -->
<input [formControl]="email" placeholder="Email" />

<!-- ✅ Good -->
<label for="email">Email address</label>
<input id="email" [formControl]="email"
       [attr.aria-invalid]="email.invalid && email.touched"
       [attr.aria-describedby]="email.invalid ? 'email-error' : null" />
<div id="email-error" *ngIf="email.invalid && email.touched" role="alert">
  Please enter a valid email address.
</div>
```

### Angular-Specific Tools
- `@angular/cdk/a11y` — `FocusTrap`, `LiveAnnouncer`, `FocusMonitor`
- `codelyzer` — a11y lint rules for Angular templates

## Svelte / SvelteKit

### Common Issues and Fixes

```svelte
<!-- ❌ Bad — on:click without keyboard -->
<div on:click={handleClick}>Action</div>

<!-- ✅ Good — Svelte a11y warning built-in -->
<button on:click={handleClick}>Action</button>

<!-- ✅ Accessible toggle -->
<button
  on:click={() => isOpen = !isOpen}
  aria-expanded={isOpen}
  aria-controls="panel"
>
  {isOpen ? 'Close' : 'Open'} Details
</button>

{#if isOpen}
  <div id="panel" role="region" aria-labelledby="toggle-btn">
    Panel content
  </div>
{/if}
```

**Note:** Svelte has built-in a11y warnings in the compiler — it flags missing alt text, click-without-keyboard, and other common issues at build time.

## Plain HTML

### Checklist for Static Sites

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Descriptive Page Title</title>
</head>
<body>
  <!-- Skip link -->
  <a href="#main" class="skip-link">Skip to main content</a>

  <header>
    <nav aria-label="Main navigation">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about" aria-current="page">About</a></li>
      </ul>
    </nav>
  </header>

  <main id="main" tabindex="-1">
    <h1>Page Heading</h1>
    <!-- Only one h1 per page -->
    <!-- Heading levels don't skip (h1 → h2 → h3, never h1 → h3) -->
  </main>

  <footer>
    <p>&copy; 2026 Company Name</p>
  </footer>
</body>
</html>
```

## CSS Accessibility Patterns

### Focus Indicators

```css
/* ❌ Bad — removes focus indicator entirely */
:focus { outline: none; }

/* ✅ Good — custom focus indicator */
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* ✅ Good — enhanced for high contrast mode */
@media (forced-colors: active) {
  :focus-visible {
    outline: 2px solid ButtonText;
  }
}
```

### Reduced Motion

```css
/* ✅ Respect prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Screen Reader Only

```css
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
```
