# Rift Draft — public five-role draft advisor (v17)

Static, privacy-friendly League of Legends draft advisor with public default settings, role-aware pick rankings, matchup coverage, five-player allied and enemy drafts, and a conditional strategic guide. Works without logins or Riot API keys.

## Publish updates to an existing GitHub Pages repository

**Replace these three files while keeping their exact paths:**

1. `site/index.html` — rebuilt public interface
2. `scripts/sync_data.py` — resilient per-role updater
3. `.github/workflows/deploy.yml` — automatic updater/deployment workflow

In GitHub, open each existing file, click its pencil/Edit button, replace the entire content with the corresponding file from this package, and commit to `main`. This avoids the hidden `.github` upload problem. If the workflow isn't present, create the file with exactly that path. Keep GitHub Pages → Source set to **GitHub Actions**.

Run **Actions → Publish Rift Draft and refresh stats → Run workflow**. Visit `https://<username>.github.io/<repository>/` after a successful run. Under **Data health**, examine each role's exact status and diagnostics; do not assume all five current snapshots exist until the published manifest says so.

## Why roles were previously marked unavailable

The original updater imposed an arbitrary minimum of 50 `matchups` keys on every dataset. Valid sparse snapshots could be rejected; other causes include upstream HTTP errors, delayed role publication, and exact patch mismatches. The rewrite validates usable data records, preserves independent role status, tries up to five earlier source patches when necessary, and labels stale snapshots. Historical results can continue to work when a current snapshot is not published. It retains the previous site's verified data as a fallback during temporary upstream outages if GitHub Pages is reachable.

The **actual cause of your specific two unavailable roles cannot be confirmed without your GitHub Actions logs or the `error` text in your published manifest**. This new updater adds that information rather than hiding it.

## Scoring

- Current patch, where available, dominates the historical blend (80% default, adjustable).
- Historical-only results are labeled; stale snapshots are not used as current-patch statistics.
- Opponent-specific Δ2 adjustments have shrinkage for sample size.
- Blind downside is included only for still-unknown opposing lane roles. Bot and Support handle both opposing duo roles.
- Champion comfort and composition heuristic adjustments are optional and **off by default**.
- All 173 champions in the original patch-26.22 roster are available. Off-role or unsupported picks are **unrated**, not given fabricated neutral scores.
- The Draft Index is not a calibrated probability of winning.

## Source and attribution

Source project: https://github.com/shizukaziye/lol-pool-coverage (Riot assets provided by Riot / CommunityDragon). The game and original IP are Riot Games properties. This is an independent third-party fan project, not endorsed by Riot Games.

## Tests

- Python updater: `python -m unittest discover -s tests -v`
- Browser smoke tested with fixture datasets for all five roles, champion search, ranked recommendations, strategic guide navigation, source-status display, and mobile width; no JS runtime errors in that fixture test.
- External live download success and GitHub deployment are **not** guaranteed until your workflow runs.
