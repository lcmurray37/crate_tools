# Crate Tools

Python utilities for building and maintaining a Rekordbox DJ library.

## Overview

This repository currently contains two standalone tools:

* **`rip_crate.py`** — Downloads audio for Spotify playlists, albums, or tracks by matching metadata against YouTube using `spotdl`.
* **`rb_genre_tagger.py`** — Uses a local Ollama LLM to generate genre suggestions for Rekordbox tracks with missing genre metadata.

---

## Requirements

* Python 3.10+
* `spotdl` (for `rip_crate.py`)
* Ollama running locally with a compatible model (default: `llama3`) for `rb_genre_tagger.py`

Example Python dependencies:

```bash
pip install pandas openpyxl openai
pip install spotdl
```

---

## `rip_crate.py`

Downloads music from Spotify playlist metadata using `spotdl`, which searches YouTube for matching audio.

### Features

* Accepts Spotify playlist, album, or track URLs
* Command-line URL input or interactive prompt
* Folder selection via Tkinter
* Downloads 320 kbps MP3 files
* Uses the active Python environment's `spotdl` installation

### Usage

```bash
python rip_crate.py
```

or

```bash
python rip_crate.py <spotify-url>
```

You will be prompted to choose a download destination.

---

## `rb_genre_tagger.py`

Scans a Rekordbox XML collection for tracks missing genre metadata and uses a locally hosted Ollama model to infer genre labels.

### Features

* Parses Rekordbox XML collections
* Detects tracks with empty genre fields
* Batch inference using the OpenAI-compatible Ollama API
* Exports suggested genres to Excel
* Generates an updated Rekordbox XML

### Configuration

Key settings are defined near the top of the script:

* Input/output file paths
* Ollama model
* Batch size

By default the script expects:

```
rekordbox_collection.xml
```

to exist in the working directory.

### Outputs

| File                              | Description                               |
| --------------------------------- | ----------------------------------------- |
| `missing_genres_suggestions.xlsx` | Suggested genre assignments for review    |
| `rekordbox_genres_updated.xml`    | Rekordbox XML with generated genre values |

### Usage

Start Ollama locally, then run:

```bash
python rb_genre_tagger.py
```

---

## Notes

* The generated XML preserves the complete Rekordbox collection and updates only tracks that received genre suggestions.
* By default, the script processes only the first batch of missing tracks (`[:15]`) as a compatibility check for local LLM output. Remove the slice to process the entire collection.
* Review generated genre suggestions before importing the updated XML into Rekordbox.

---

## Disclaimer

These utilities are intended for personal music library management.

Users are responsible for complying with applicable copyright laws, platform terms of service, and licensing requirements in their jurisdiction.