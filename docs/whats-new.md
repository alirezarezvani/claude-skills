---
title: "What's New"
description: "Release notes for the claude-skills library, generated from CHANGELOG.md at build time. Currently at v{{ count.version }} with {{ count.skills }} skills."
---

# What's New

The library is at **v{{ count.version }}**: {{ count.skills }} skills, {{ count.plugins }} plugins, {{ count.agents }} agents and {{ count.commands }} commands across {{ count.domains }} domains.

This page is built from [CHANGELOG.md](https://github.com/alirezarezvani/claude-skills/blob/main/CHANGELOG.md) every time the site deploys, so it always shows the latest five releases. To pull a release into an existing install:

```text
/plugin marketplace update claude-code-skills
/plugin update
```

---

{{ whats_new }}
