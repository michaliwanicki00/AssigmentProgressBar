# Assignment Progress Bar

A tiny desktop app that tracks progress on the Big Data Processing – Functional
Programming assignment (`fp_template`): 4 parts, 29 questions, 125 points.

Tick the questions you have finished and each part's progress bar — plus a
combined 0–125 bar — fills by that question's point value. Your ticks are saved
between runs in `progress_bar_data.json` (next to the script).

## Running it

Needs Python 3 with tkinter (bundled with the standard Windows/macOS installers).
No third-party packages.

- **Windows:** double-click `progress_bar.pyw`, or run `Progress Bar.bat`.
- **Any OS:** `python progress_bar.pyw`

## Files

| File | Purpose |
|------|---------|
| `progress_bar.pyw` | The whole app (standard library only). |
| `Progress Bar.bat` | Windows launcher (`pythonw`, no console window). |
| `progress_bar_data.json` | Auto-created; stores which questions are ticked. Git-ignored by default. |
