# Next-New-Repo-Watch

## Issue Log

- **2026-10-10 — Transcript error caused a false repository match.** YouTube transcript requests were blocked from the cloud IP, and the unavailable-transcript error body contains links to `jdepoix/youtube-transcript-api`. The extractor previously combined that error text with the video description, incorrectly treating the helper project as featured. `scripts/watch.py` now extracts from the description alone whenever the transcript is unavailable; normal transcript extraction is unchanged. A fixture verified that a valid description repo is retained and the error-only repo is excluded. Reports disclose the transcript limitation and use available descriptions plus current GitHub evidence.
