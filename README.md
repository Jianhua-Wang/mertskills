# mertskills

Agent skills for scientific work: figures, manuscript prose, peer review and
talks. Each top-level folder is one skill with its own `SKILL.md`.

| Skill | What it does |
|---|---|
| `figure-forge` | Publication-quality matplotlib figures: one semantic palette, journal typography, legends kept in sync with the data. |
| `paper-prose` | Drafts, revises and de-AIs English manuscript prose, from title to figure legends and reviewer responses. |
| `peer-review` | Writes and checks peer-review reports, reviewer-form answers and Chinese thesis evaluations. |
| `slide-studio` | Academic PowerPoint decks on one fixed template, built from a YAML spec, linted and rendered for QA. |

## Install

Install with the [`skills`](https://www.npmjs.com/package/skills) CLI (needs
Node.js). `-g` installs for your user instead of one project, and `-a` picks
the agent.

One skill:

```bash
npx skills add Jianhua-Wang/mertskills --skill slide-studio -g -a claude-code -y
```

Every skill in this repo:

```bash
npx skills add Jianhua-Wang/mertskills --skill '*' -g -a claude-code -y
```

For Codex as well, add `-a codex`. To see what the repo offers without
installing anything, run `npx skills add Jianhua-Wang/mertskills --list`.

## Update

`update` pulls the latest version from GitHub, so a change reaches other
machines only after it is pushed.

```bash
npx skills update slide-studio -g
```

To update every installed skill at once:

```bash
npx skills update -g
```

`update` only touches skills that `npx skills add` installed. Add a new skill
from this repo with `add` first.

## Developing a skill

On the machine where you edit the skills, link the clone into the agent's
skill folder so edits take effect at once:

```bash
git clone https://github.com/Jianhua-Wang/mertskills.git ~/mertskills
```

```bash
ln -s ~/mertskills/slide-studio ~/.claude/skills/slide-studio
```

A linked skill updates with `git pull`, not `npx skills update`. Don't install
the same skill both ways on one machine.

## Requirements

- `slide-studio` scripts run with [uv](https://docs.astral.sh/uv/) and declare
  their own dependencies. The scripts in `paper-prose` and `peer-review` run
  with Python 3. `peer-review` also needs PyMuPDF, Pillow, openpyxl and
  python-docx for some file types.
- `slide-studio` renders decks for QA with Microsoft PowerPoint on macOS, or
  LibreOffice as a fallback. Its fonts, Arial and DengXian, ship with
  Microsoft Office.
