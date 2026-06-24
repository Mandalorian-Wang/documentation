# Contribute to the documentation

Thanks for contributing to the BoxLite documentation. This guide is the **single
source of truth** for how to make changes locally and how to ship them.

## Setup (once)

```bash
git clone https://github.com/boxlite-ai/documentation.git
cd documentation
npm i -g mint    # Mintlify CLI (Node 18+)
brew install gh  # GitHub CLI, used by deploy:preview
```

## The four commands

The same four `npm` scripts exist in every BoxLite content repo (`documentation`,
`boxlite-website`, `boxlite-blog`) so the workflow is identical everywhere.

| Command | What it does | When to use |
|---|---|---|
| `npm run dev` | Local preview at http://localhost:3000 (`mint dev`) | While editing |
| `npm run check` | `mint validate && mint broken-links` | Before opening / updating a PR |
| `npm run deploy:preview` | Pushes the current branch and opens (or reuses) a PR; Mintlify auto-builds a `*.mintlify.app` preview tied to that PR | To share work for review |
| `npm run deploy:production` | Production = `main` only. Guards: must be on `main`, clean worktree, in sync with `origin/main`. Then instructs you to `gh pr merge` — merging a PR is the deploy. | To ship the docs |

### One canonical lifecycle (memorize this)

```
①  git switch -c your-change         from main
②  edit pages
③  npm run dev                       preview locally
④  git commit -am "..."
⑤  npm run check                     validate + broken-links
⑥  npm run deploy:preview            push + open PR; Mintlify builds preview
⑦  review the *.mintlify.app preview (light/dark, desktop/mobile)
⑧  npm run deploy:production         on main → prints the merge command
⑨  gh pr merge <PR#> --merge --delete-branch
                                     main updates → Mintlify auto-deploys
                                     https://docs.boxlite.ai
```

## Rules of the road

- **`main` is protected.** Never push to it directly. Production happens only by
  **merging a PR**. There is no "deploy to production" command — `npm run deploy:production`
  guards the preconditions and tells you the merge command to run.
- **Preview = PR.** Mintlify builds the preview when a PR is opened against `main`
  (not on a bare branch push). The Mintlify bot posts the `*.mintlify.app` link as a
  PR comment, and rebuilds on every push to the PR branch.
- **`deploy:preview` may include just-committed work** that hasn't been reviewed —
  it is not a review artifact on its own. The *PR review* is.
- **Why Docs has no `vercel`-style CLI deploy:** Mintlify only publishes through its
  Git integration; it has no production CLI deploy. The sibling Vercel repos
  (`boxlite.ai`, `blog.boxlite.ai`) follow the same lifecycle and use the same
  four script names; their `deploy:preview` shells out to `vercel deploy` because
  Vercel does have a CLI. The mental model is identical across all three repos.

## Edit on GitHub (no clone)

1. Open the page on github.com/boxlite-ai/documentation.
2. Click the pencil (**Edit this file**) icon — GitHub forks for you.
3. Open a pull request. Mintlify will post a preview link on the PR.

## Writing guidelines

- **Active voice**: "Run the command", not "The command should be run".
- **Address the reader directly** with "you".
- **One idea per sentence.**
- **Lead with the goal**, then the action.
- **Use consistent terminology** — don't alternate synonyms for the same concept.
- **Show, don't just tell** — include realistic examples.
