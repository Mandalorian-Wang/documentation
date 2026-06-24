# Contribute to the documentation

Thanks for contributing to the BoxLite documentation! This guide covers how to
make changes locally and the **one** path those changes take to production.

## How to contribute

### Option 1 — Edit on GitHub

1. Navigate to the page you want to edit.
2. Click the pencil (**Edit this file**) icon.
3. Make your changes and open a pull request.

### Option 2 — Local development

1. Fork and clone this repository.
2. Install the Mintlify CLI: `npm i -g mint`
3. Create a branch: `git switch -c your-change`
4. Edit the `.mdx` pages or `docs.json`.
5. Preview locally: `mint dev` → http://localhost:3000
6. Before pushing, check links: `mint broken-links`
7. Commit and open a pull request.

## Deployment — one standard path

This site is hosted by **Mintlify** (not Vercel) and is **fully Git-driven**.
There are no deploy scripts and no `vercel` / CLI publish commands in this repo —
please don't add any. Every change, from everyone, follows the same path:

```
①  branch from main       git switch -c <branch>
②  edit + local preview   mint dev              → localhost:3000
③  push + open a PR        git push -u origin <branch>  (then open the PR)
                          → Mintlify builds a Preview automatically (~1 min)
④  review on the Preview   light/dark · desktop/mobile · nav · code blocks
⑤  merge the PR into main → Mintlify deploys Production → docs.boxlite.ai
```

Rules of the road:

- **`main` is protected — never push to it directly.** Production happens only by
  merging a PR. There is no "deploy to production" command; the merge *is* the deploy.
- **Preview = pull request.** Mintlify creates the preview when a PR is opened
  against `main` (not on a bare branch push). The Mintlify bot posts the
  `*.mintlify.app` preview link as a PR comment, and it rebuilds on every push to
  the PR branch.
- **Quick local look?** Use `mint dev`. There is no "deploy preview" command for
  docs — open a PR to share a preview.
- **Pre-review check:** run `mint broken-links` (and optionally `mint validate`)
  before requesting review.

> **Why no CLI deploy here:** Mintlify only publishes through its Git integration —
> it has no production CLI deploy. The sibling sites `boxlite.ai` and
> `blog.boxlite.ai` live in separate Vercel repos and follow the *same* mental
> model (branch → PR → preview → merge → production); those repos additionally keep
> a `vercel` CLI only for throwaway local previews. This docs repo does not — keep
> it Git-driven so there is exactly one way to ship.

## Writing guidelines

- **Use active voice**: "Run the command" not "The command should be run"
- **Address the reader directly**: use "you" instead of "the user"
- **Keep sentences concise**: aim for one idea per sentence
- **Lead with the goal**: start instructions with what the reader wants to accomplish
- **Use consistent terminology**: don't alternate between synonyms for the same concept
- **Include examples**: show, don't just tell
