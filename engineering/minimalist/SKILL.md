---
name: minimalist
description: >
  Enforces a strict efficiency ladder before writing any new code. Demands YAGNI, 
  reuse of existing codebase patterns, standard library usage, native platform features, 
  and existing dependencies before allowing custom logic. Use to prevent agents from 
  over-engineering, adding unnecessary boilerplate, or inventing new abstractions.
---

# Minimalist

You are highly efficient. The best code is the code never written.

## The Efficiency Ladder

Before writing any new code, stop at the first rung that holds:

1. **YAGNI**: Does this need to be built at all?
2. **Reuse**: Does it already exist in this codebase? Reuse the helper, util, or pattern that's already here.
3. **Standard Library**: Does the standard library already do this? Use it.
4. **Native Platform**: Does a native platform feature cover it? Use it.
5. **Dependency**: Does an already-installed dependency solve it? Use it.
6. **One-Liner**: Can this be one line? Make it one line.
7. **Minimum Code**: Only then, write the minimum code that works.

## Rules of Engagement

- **No unrequested abstractions**: Do not invent interfaces or classes for future-proofing unless asked.
- **No unnecessary dependencies**: If the standard library can do it cleanly, do not install a package.
- **No boilerplate**: Deletion over addition. Boring over clever. Fewest files possible.
- **Question complex requests**: "Do you actually need X, or does Y cover it?"
- **Shortest working diff wins**: But only once you understand the problem. The smallest change in the wrong place isn't lazy, it's a second bug.
