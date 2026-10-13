# 115-1 Study Workspace

Independent course hub: https://zi-yiii.github.io/115-1/

- Pathology home: `pathology/`. Existing Micro tools stay at their original URLs.
- Pharmacology home: `pharmacology/`; Block 1 reserved, Block 2 available.
- Master tables: reserved in the main hub.

## Sync reviewed pharmacology HTML

```sh
python3 scripts/sync-pharmacology.py --source <reviewed-html-folder>
```

Publish from `main`, repository root. `?embed=1` hides navigation on standalone learning pages.
