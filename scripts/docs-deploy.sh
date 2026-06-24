#!/usr/bin/env bash
# docs-deploy.sh — uniform deploy entry for the Mintlify docs repo.
#
# Mirrors the boxlite-website / boxlite-blog vercel-deploy.sh in shape, so a
# contributor moving between the three repos uses the same commands:
#
#   preview     push current branch + ensure a PR exists.
#               Mintlify builds a *.mintlify.app preview tied to the PR.
#               May include just-committed work; not for production.
#
#   production  guarded: must be on main, clean worktree, ahead of origin/main.
#               Production happens by `gh pr merge` (because main is protected
#               and Mintlify is git-driven — there is no `mint deploy`).
#
# Why no CLI prod push: Mintlify has no production CLI deploy; it only ships
# what lands on main. main is protected on GitHub, so production is always
# "merge the PR". This script makes that the one explicit command.

set -euo pipefail

MODE="${1:-preview}"
REPO_SLUG="boxlite-ai/documentation"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "✗ '$1' not installed. $2" >&2; exit 1; }
}

is_clean_worktree() {
  git diff --quiet && git diff --cached --quiet \
    && [ -z "$(git ls-files --others --exclude-standard)" ]
}

ensure_clean_worktree() {
  if ! is_clean_worktree; then
    echo "✗ Worktree is dirty. Production requires a clean tree." >&2
    git status --short >&2
    exit 1
  fi
}

ensure_main_branch() {
  local branch
  branch="$(git branch --show-current)"
  if [ "$branch" != "main" ]; then
    echo "✗ Production only deploys from 'main' (current: $branch)." >&2
    echo "  Switch to main, sync, then re-run." >&2
    exit 1
  fi
}

ensure_main_in_sync() {
  git fetch origin main >/dev/null
  local local_sha remote_sha merge_base
  local_sha="$(git rev-parse HEAD)"
  remote_sha="$(git rev-parse origin/main)"
  merge_base="$(git merge-base HEAD origin/main)"
  if [ "$merge_base" != "$remote_sha" ] && [ "$local_sha" != "$remote_sha" ]; then
    echo "✗ Local main is behind/diverged from origin/main. Run: git pull --ff-only" >&2
    exit 1
  fi
}

case "$MODE" in
  preview)
    require_cmd git "Install git."
    require_cmd gh  "Install GitHub CLI: https://cli.github.com"

    local_branch="$(git branch --show-current)"
    if [ "$local_branch" = "main" ]; then
      echo "✗ Cannot preview from main. Create a branch:" >&2
      echo "    git switch -c your-change" >&2
      exit 1
    fi

    if ! is_clean_worktree; then
      echo "⚠ Worktree has uncommitted changes. Preview only ships committed work."
      echo "  Commit first, then re-run, or push then push --force-with-lease later."
      git status --short
      exit 1
    fi

    echo "▶ Pushing '$local_branch' to origin..."
    git push -u origin "$local_branch"

    if pr_url=$(gh pr view --json url --jq .url 2>/dev/null); then
      echo "▶ PR already open: $pr_url"
    else
      echo "▶ Opening PR against main..."
      gh pr create --repo "$REPO_SLUG" --base main --head "$local_branch" --fill
      pr_url=$(gh pr view --json url --jq .url)
    fi

    echo ""
    echo "✓ Push + PR done. Mintlify builds the preview automatically (~1 min)."
    echo "  Watch for the mintlify[bot] comment on: $pr_url"
    echo "  Preview URL format: https://boxliteai-<branch-slug>.mintlify.app"
    ;;

  production)
    require_cmd git "Install git."

    ensure_main_branch
    ensure_clean_worktree
    ensure_main_in_sync

    echo "✓ On main, clean, in sync with origin/main."
    echo ""
    echo "Production = merging a PR into main (main is protected; merge is the deploy)."
    echo "Find and merge the docs PR:"
    echo "    gh pr list --repo $REPO_SLUG --base main"
    echo "    gh pr merge <NUMBER> --repo $REPO_SLUG --merge --delete-branch"
    echo ""
    echo "Once main updates, Mintlify auto-deploys https://docs.boxlite.ai (~1 min)."
    ;;

  *)
    echo "usage: $0 {preview|production}" >&2
    exit 2
    ;;
esac
