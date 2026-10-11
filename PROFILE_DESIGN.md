# Electric Defense — profile visual system

The profile uses original electric-blue and purple SVG artwork. Personal
information, skills, featured project descriptions, and PROJECT_SHOWCASE.md
remain the source content; the visual layer does not add certifications or
claims about project readiness.

## What runs on GitHub

- Self-contained SVG images: lightning, sliced-text glitches, falling code,
  orbiting rings, typing, project illustrations, and moving section dividers.
- Normal Markdown links and linked project images.
- Native `details` / `summary` project panels and section anchors.
- No README JavaScript, external CSS, iframe, video background, or simulated
  hover interaction. A project illustration links as one complete image.
- Internal SVG CSS honors `prefers-reduced-motion`. Non-animated renderers still
  display the complete artwork and essential text. The role line is also plain
  Markdown so it remains available throughout the typing cycle.

## Activity data and automation

`scripts/update_activity.py` reads the calendar shown on the public GitHub
contributions page. Dates, counts, and activity levels are copied from that
page; animation never changes the data. No personal access token or external
statistics service is needed for the main charts. The snapshot includes the
same aggregate activity GitHub exposes publicly, not repository contents.

The monthly chart sums those calendar days. The first and last month can be
partial. Counts are activity, not a skill rating. Both charts have a consistent
date range, and the calendar shows its snapshot date.

The `Refresh profile visuals` workflow runs daily at 02:23 UTC, on changes to
its generator/workflow, or through **Run workflow**. It regenerates assets,
validates them, and commits only changed files in `assets/` using the standard
repository `GITHUB_TOKEN`. It has only `contents: write` permission; the official
checkout action is pinned to a commit. No new secrets are needed.

If the public calendar markup changes or a request fails, generation fails
before overwriting the last good snapshot. The date on the graphic therefore
also makes a stale snapshot visible. Scheduled workflows in inactive public
repositories may be disabled by GitHub; they can be re-enabled in Actions.

The optional language card still uses its existing third-party service. Main
profile artwork and activity charts are stored in this repository.

## Rebuild

Python 3.10+; standard library only:

```sh
python3 scripts/build_visuals.py
python3 scripts/update_activity.py --username Dinesh-757
python3 scripts/validate_profile.py
```

SVGs stay at their existing paths so project dossier artwork remains linked.
The contribution snapshot is saved for inspection and reproducibility.
