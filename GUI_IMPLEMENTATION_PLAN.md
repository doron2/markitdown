# MarkItDown GUI — Implementation Progress

Based on `claude-code-kickoff.md`. Each checkpoint must pass before the next step starts.
Activate venv before any Python/PyInstaller commands: `source .venv/bin/activate`

---

## CP-0 — Remotes & tracker
- [ ] `git remote -v` shows `origin` (doron2) AND `upstream` (microsoft)
- [ ] This file exists at the repo root

## CP-1 — Branch
- [ ] Active branch is `gui` (`git branch` shows `* gui`)

## CP-2 — Python environment
- [ ] `python -c "from markitdown import MarkItDown; print('ok')"` → `ok`
- [ ] `python -m PyInstaller --version` → prints version
- [ ] `python -c "import tkinter; print(tkinter.TkVersion)"` → `8.6`

## CP-3 — GUI app (`gui/app.py`)
- [ ] `python gui/app.py` opens the window without errors
- [ ] Select a real file, Convert, see `✓ done` in status area
- [ ] `.md` output written to correct location
- [ ] UI does not freeze during conversion (background thread)

## CP-4 — Linux binary
- [ ] `dist/markitdown-gui` exists and is executable
- [ ] `./dist/markitdown-gui` opens the GUI (no import errors)
- [ ] PDF → non-empty `.md` ✓
- [ ] DOCX → non-empty `.md` ✓
- [ ] HTML → non-empty `.md` ✓

## CP-5 — GitHub Actions workflow
- [ ] `.github/workflows/build-gui-release.yml` exists
- [ ] YAML valid (`python3 -c "import yaml; yaml.safe_load(open('.github/workflows/build-gui-release.yml'))"`)
- [ ] Matrix has 3 entries (windows, ubuntu, macos)
- [ ] `release` job has `needs: build`

## CP-6 — Docs & .gitignore
- [ ] `git status` shows only expected files (no `dist/` or `build/`)
- [ ] `python gui/app.py` still opens cleanly
- [ ] README has GUI section with download + run-from-source instructions

## CP-7 — Commit, push, tag
- [ ] Commit on branch `gui` with message "Add Tkinter GUI..."
- [ ] `git tag` shows `v0.1.0`
- [ ] GitHub push succeeded
- [ ] Actions run visible at https://github.com/doron2/markitdown/actions
- [ ] Releases page URL provided to user

---

## Resuming a session

1. `cd /home/imagry/Desktop/projects/markitdown`
2. `git checkout gui`
3. `source .venv/bin/activate`
4. Read this file, find the first unchecked box, resume from there.
