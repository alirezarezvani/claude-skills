# Framework-Specific Patterns

Quick reference for identifying routes, components, state, and APIs across frontend frameworks.

## React (CRA / Vite)

| Aspect | Where to Look |
|--------|--------------|
| Routes | `react-router-dom` — `<Route path="...">` or `createBrowserRouter` |
| Components | `.tsx` / `.jsx` files, default exports |
| State | Redux (`store/`), Zustand, Jotai, Recoil, React Context |
| API | `axios`, `fetch`, TanStack Query (`useQuery`), SWR (`useSWR`) |
| Forms | React Hook Form, Formik, Ant Design Form, custom `useState` |
| i18n | `react-i18next`, `react-intl` |

## Next.js (App Router)

| Aspect | Where to Look |
|--------|--------------|
| Routes | `app/` directory — `page.tsx` = route, folders = segments |
| Layouts | `layout.tsx` per directory |
| Loading | `loading.tsx`, `error.tsx`, `not-found.tsx` |
| API routes | `app/api/` or `pages/api/` (Pages Router) |
| Server actions | `"use server"` directive |
| Middleware | `middleware.ts` at root |

## Next.js (Pages Router)

| Aspect | Where to Look |
|--------|--------------|
| Routes | `pages/` directory — filename = route |
| Data fetching | `getServerSideProps`, `getStaticProps`, `getStaticPaths` |
| API routes | `pages/api/` |

## Vue 3

| Aspect | Where to Look |
|--------|--------------|
| Routes | `vue-router` — `routes` array in `router/index.ts` |
| Components | `.vue` SFCs (`<template>`, `<script setup>`, `<style>`) |
| State | Pinia (`stores/`), Vuex (`store/`) |
| API | `axios`, `fetch`, VueQuery |
| Forms | VeeValidate, FormKit, custom `ref()` / `reactive()` |
| i18n | `vue-i18n` |

## Nuxt 3

| Aspect | Where to Look |
|--------|--------------|
| Routes | `pages/` directory (file-system routing) |
| Layouts | `layouts/` |
| API routes | `server/api/` |
| Data fetching | `useFetch`, `useAsyncData`, `$fetch` |
| State | `useState`, Pinia |
| Middleware | `middleware/` |

## Angular

| Aspect | Where to Look |
|--------|--------------|
| Routes | `app-routing.module.ts` or `Routes` array |
| Components | `@Component` decorator, `*.component.ts` |
| State | NgRx (`store/`), services with `BehaviorSubject` |
| API | `HttpClient` in services |
| Forms | Reactive Forms (`FormGroup`), Template-driven forms |
| i18n | `@angular/localize`, `ngx-translate` |
| Guards | `CanActivate`, `CanDeactivate` |

## Svelte / SvelteKit

| Aspect | Where to Look |
|--------|--------------|
| Routes | `src/routes/` (file-system routing with `+page.svelte`) |
| Layouts | `+layout.svelte` |
| Data loading | `+page.ts` / `+page.server.ts` (`load` function) |
| API routes | `+server.ts` |
| State | Svelte stores (`writable`, `readable`, `derived`) |

## Common Patterns Across Frameworks

### Mock Detection
```
# Likely mock
setTimeout(() => resolve(data), 500)
Promise.resolve(mockData)
import { data } from './fixtures'
faker.name.firstName()

# Likely real
axios.get('/api/users')
fetch('/api/data')
httpClient.post(url, body)
useSWR('/api/resource')
```

### Permission Patterns
```
# React
{hasPermission('admin') && <Button>Delete</Button>}
<ProtectedRoute roles={['admin', 'manager']}>

# Vue
v-if="user.role === 'admin'"
v-permission="'user:delete'"

# Angular
*ngIf="authService.hasRole('admin')"
canActivate: [AuthGuard]
```

### Form Validation
```
# React Hook Form
{ required: 'Name is required', maxLength: { value: 50, message: 'Too long' } }

# VeeValidate (Vue)
rules="required|email|max:100"

# Angular Reactive Forms
Validators.required, Validators.minLength(3), Validators.pattern(...)
```
