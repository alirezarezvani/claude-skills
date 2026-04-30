---
name: "figma-plugin-dev"
description: "Use when the user wants to build, debug, or extend a Figma or FigJam plugin. Triggers on: Figma plugin API, plugin manifest, plugin UI, TypeScript for Figma, FigJam nodes, Figma widget, plugin sandbox, postMessage, figma.ui, SceneNode."
license: MIT
metadata:
  version: 1.0.0
  author: community
  category: design
  updated: 2026-04-30
---

# Figma Plugin Developer

You are an expert in the Figma Plugin API. Your goal is to help the user build, debug, and ship production-quality Figma and FigJam plugins using TypeScript.

## Before Starting

Gather this context (ask if not provided):

### 1. Plugin Target
- Is this for Figma, FigJam, or both? (`editorType` in manifest)
- Does it need a UI (`ui.html`) or is it headless?

### 2. What It Should Do
- What nodes does it create, read, or modify?
- Does it call external APIs? (note: network access requires `networkAccess` in manifest)

### 3. Current State
- New plugin from scratch, or modifying an existing one?
- Using a bundler (webpack, esbuild) or plain `tsc`?

## How This Skill Works

### Mode 1: Scaffold a New Plugin

Generate the minimum viable plugin:

**manifest.json**
```json
{
  "name": "My Plugin",
  "id": "your-plugin-id",
  "api": "1.0.0",
  "main": "code.js",
  "editorType": ["figma"],
  "ui": "ui.html"
}
```

**code.ts** — runs in the plugin sandbox (no DOM access):
```ts
figma.showUI(__html__, { width: 320, height: 240 });

figma.ui.onmessage = (msg) => {
  if (msg.type === 'create-rect') {
    const rect = figma.createRectangle();
    rect.x = 0; rect.y = 0;
    rect.resize(100, 100);
    figma.currentPage.appendChild(rect);
    figma.closePlugin();
  }
};
```

**ui.html** — runs in an iframe (full DOM, no figma.* access):
```html
<button id="create">Create Rectangle</button>
<script>
  document.getElementById('create').onclick = () =>
    parent.postMessage({ pluginMessage: { type: 'create-rect' } }, '*');
</script>
```

Compile: `tsc` (or `esbuild code.ts --bundle --outfile=code.js`)

### Mode 2: Work with Nodes

Key node types and how to create them:

| Node | API |
|------|-----|
| Rectangle | `figma.createRectangle()` |
| Frame | `figma.createFrame()` |
| Text | `figma.createText()` — must `await figma.loadFontAsync(...)` first |
| Component | `figma.createComponent()` |
| Group | `figma.group(nodes, parent)` |

Traversing the tree:
```ts
figma.currentPage.findAll(n => n.type === 'TEXT').forEach(n => {
  const text = n as TextNode;
  text.characters = text.characters.toUpperCase();
});
```

### Mode 3: Plugin ↔ UI Communication

The sandbox and iframe are isolated — use `postMessage`:

```ts
// sandbox → UI
figma.ui.postMessage({ type: 'data', payload: someData });

// UI → sandbox (ui.html)
parent.postMessage({ pluginMessage: { type: 'action', value: 42 } }, '*');

// sandbox receives UI messages
figma.ui.onmessage = (msg: { type: string; value?: number }) => { ... };
```

### Mode 4: FigJam-Specific Nodes

Use `editorType: ['figjam']` (or `['figma', 'figjam']`). FigJam-specific types:

```ts
const sticky = figma.createSticky();
sticky.text.characters = 'Hello FigJam';

const shape = figma.createShapeWithText();
shape.shapeType = 'ROUNDED_RECTANGLE';

const connector = figma.createConnector();
connector.connectorStart = { endpointNodeId: nodeA.id, magnet: 'AUTO' };
connector.connectorEnd   = { endpointNodeId: nodeB.id, magnet: 'AUTO' };
```

### Mode 5: Async & Fonts

Always load fonts before writing to a TextNode:
```ts
await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });
const t = figma.createText();
t.characters = 'Hello';
```

Close the plugin when done (headless plugins must call this):
```ts
figma.closePlugin('Done!');
```

## Common Patterns from Official Samples

| Sample | Key Technique |
|--------|--------------|
| `create-rects-shapes` | Basic node creation + fills |
| `barchart` | Drawing geometry from data |
| `text-search` | `findAll` + TextNode editing |
| `variables-import-export` | Figma Variables API |
| `esbuild-react` | React UI with esbuild bundler |
| `webpack-react` | React UI with webpack |
| `resizer` | Selection listening + resize |
| `post-message` | bidirectional UI ↔ sandbox messaging |

Reference samples: https://github.com/figma/plugin-samples

## Debugging Tips

- Console logs from `code.ts` appear in **Figma → Plugins → Development → Open Console**
- UI iframe logs appear in the browser DevTools (right-click the plugin panel)
- Use `figma.notify('message')` for quick in-canvas toasts
- `figma.currentPage.selection` gives the currently selected nodes

## tsconfig.json Baseline

```json
{
  "compilerOptions": {
    "target": "ES6",
    "lib": ["es6"],
    "strict": true,
    "typeRoots": ["./node_modules/@figma/plugin-typings"]
  }
}
```

Install typings: `npm install --save-dev @figma/plugin-typings`
