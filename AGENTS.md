# BoxLite Documentation — Agent Instructions

This is the official documentation site for **BoxLite**, built with Mintlify. BoxLite is a local-first micro-VM sandbox for AI agents — stateful, lightweight, hardware-level isolation, no daemon required.

## Project Structure

- `docs.json` — Mintlify config (navigation, theme, colors, logo). Check before making structural changes.
- `index.mdx` — Home page
- `getting-started/` — Quickstart guides (Python, Node.js, Rust, C)
- `architecture/` — Architecture deep dives (components, security, networking)
- `reference/` — SDK API reference (`python/`, `nodejs/`, `rust/`, `c/`)
- `guides/` — How-to guides (build from source, examples, AI integration, etc.)
- `development/` — Internal docs (CLI, Rust style guide)
- `snippets/` — Reusable MDX snippets (included via `<Snippet file="..." />`)
- `images/`, `logo/` — Static assets

## Development Commands

```bash
mint dev              # Local preview at http://localhost:3000
mint broken-links     # Check for broken links
mint update           # Update Mintlify CLI
```

## Navigation

Navigation is defined in `docs.json` under `navigation.tabs` with 4 tabs:
1. **Documentation** — Getting Started, Architecture, FAQ
2. **SDK Reference** — Python, Node.js, Rust, C SDK reference pages
3. **Guides** — How-to guides
4. **Development** — CLI docs, Rust style guide

Rules:
- Never add a page to navigation without creating the `.mdx` file first
- Never remove a page without checking for inbound links from other pages
- Navigation order in `docs.json` determines sidebar order

## Writing Conventions

### Frontmatter (required on every page)
```yaml
---
title: "Page Title"
description: "One-line description for SEO and navigation"
sidebarTitle: "Short Nav Title"  # optional, if nav title differs
---
```

### Style
- Active voice, second person ("you")
- Sentence case for headings
- Bold for UI elements: Click **Settings**
- Code formatting for: file names, commands, paths, code references
- One idea per sentence
- Lead instructions with the goal, not the action

### Code Blocks
- Always include language identifier: ` ```python `, ` ```bash `, etc.
- Add filename title when relevant: ` ```python main.py `
- Use realistic parameter values, not `foo`/`bar`
- Include error handling in API examples

### MDX Components
Use Mintlify's built-in components — prefer them over raw HTML:
- `<Card>`, `<CardGroup>` — navigation cards
- `<Note>`, `<Warning>`, `<Tip>`, `<Info>` — callout boxes
- `<Tabs>`, `<Tab>` — tabbed content (e.g., platform-specific instructions)
- `<Snippet file="filename.mdx" />` — reusable content from `snippets/`
- Full reference: https://mintlify.com/docs/components

## Terminology

Use these terms consistently:
- **BoxLite** — product name (capital B, capital L)
- **LiteBox** — the VM instance type
- **box** — generic reference to a sandbox instance (lowercase)
- **SimpleBox / CodeBox / BrowserBox** — Python SDK box types
- **Guest Agent** — agent running inside the VM
- **Jailer** — security isolation component
- **ShimController** — process lifecycle manager

## What to Avoid

- Don't edit `docs.json` without understanding the full navigation structure
- Don't use HTML when an MDX component exists for the same purpose
- Don't add pages to navigation that don't have corresponding `.mdx` files
- Don't alternate between synonyms for the same concept (pick one term, stick with it)

---

## Automated Documentation Sync

This section is for the Claude Code agent running in the `sync-from-boxlite` GitHub Actions workflow. When a PR merges in `boxlite-ai/boxlite`, this agent analyzes the diff and updates documentation accordingly.

### Source-to-docs mapping

Use this table to determine which documentation files to update based on changed source files in the boxlite repo.

| BoxLite source path | Documentation files to check |
|---|---|
| `sdk/python/**` | `reference/python/*.mdx`, `getting-started/quickstart-python.mdx` |
| `sdk/nodejs/**` | `reference/nodejs/*.mdx`, `getting-started/quickstart-nodejs.mdx` |
| `sdk/rust/**`, `boxlite-sdk/` | `reference/rust/*.mdx`, `getting-started/quickstart-rust.mdx` |
| `sdk/c/**`, `boxlite-c/` | `reference/c/*.mdx`, `getting-started/quickstart-c.mdx` |
| `src/vmm/**`, `src/jailer/**` | `architecture/components.mdx`, `architecture/security.mdx` |
| `src/networking/**` | `architecture/networking-storage.mdx` |
| `src/guest_agent/**` | `architecture/components.mdx` |
| `README.md`, `CHANGELOG.md` | `guides/changelog.mdx`, `index.mdx` |
| `examples/**` | `tutorials/*.mdx`, `guides/*.mdx` |
| `Cargo.toml`, `pyproject.toml`, `package.json` | Check for dependency or feature changes that affect quickstarts |

### Decision framework

Decide whether to update docs based on the nature of the change:

**Update docs when:**
- Public API added, changed, or removed (new methods, changed parameters, renamed types)
- New SDK feature or capability (new box type, new configuration option)
- Behavior change that affects users (default values changed, error handling updated)
- New examples or tutorials added upstream
- Installation or setup process changed
- New platform support or requirements changed

**Skip docs update when:**
- Internal refactoring with no public API change
- Test-only changes
- CI/CD pipeline changes in boxlite repo
- Code comments or internal documentation changes
- Performance optimizations with no API/behavior change
- Dependency bumps with no user-facing effect

**When unsure:** Create the PR anyway with a note explaining what changed and why you're unsure whether docs need updating. Let the human reviewer decide.

### PR and commit conventions

- **Branch name**: `docs-sync/boxlite-pr-{N}` where `{N}` is the source PR number
- **Commit message**: `docs: update {area} from boxlite PR #{N}` (e.g., `docs: update Python SDK reference from boxlite PR #142`)
- **PR title**: `docs: sync from boxlite PR #{N}`
- **PR body**: Include a link to the source PR and a summary of what changed and why
- **No version numbers**: Never add version numbers anywhere in documentation. Always describe features as current behavior.
