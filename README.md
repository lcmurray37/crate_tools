# Crate Tools

A collection of Python utilities for managing and expanding a Rekordbox music library.

## Overview

This repository contains two primary scripts:
- **`rip_crate.py`** – Downloads audio corresponding to Spotify playlists by matching playlist metadata against YouTube using `spotdl`, then formats the downloaded files for inclusion in a DJ library.
- **`rb_genre_tagger.py`** – Uses a local Ollama large language model to analyze tracks in a Rekordbox collection that are missing genre information and generates suggested genre tags for manual review.

---

# rip_crate.py

## Purpose

This utility automates downloading music that corresponds to a Spotify playlist by searching YouTube using playlist metadata.

It uses `spotdl` to locate and download matching audio and provides a simple graphical interface built with Tkinter.

## Features

- Tkinter GUI
- Spotify playlist support
- Uses `spotdl` for YouTube matching and downloads
- Organizes downloaded files into a destination folder
- Automatically formats downloaded tracks for easier library management

## Download Method

The script attempts to locate YouTube uploads that best match the metadata contained in a Spotify playlist.

Because it relies primarily on metadata matching rather than direct audio extraction from Spotify, this workflow is generally considered a safe and practical approach for obtaining publicly available YouTube audio.

---

# Requirements

Typical dependencies include:

- Python 3.10+
- Ollama (running locally)
- spotdl
- Tkinter
- pandas
- openpyxl
- lxml (if applicable)

Install Python dependencies with:

```bash
pip install -r requirements.txt
```

---

# Workflow

### Genre Tagging

1. Export your Rekordbox collection as XML.
2. Run `rb_genre_tagger.py`.
3. Review the generated Excel file.
4. Apply or verify the suggested genres.
5. Import `rekordbox_genres_updated.xml` back into Rekordbox.

### Playlist Ripping

1. Launch `rip_crate.py`.
2. Enter or select a Spotify playlist.
3. Choose a destination folder.
4. Download matching tracks from YouTube via `spotdl`.
5. Import the formatted files into your music library.

---

# rb_genre_tagger.py

## Purpose

Many music libraries contain tracks without consistent genre metadata. This script scans a Rekordbox XML collection, identifies tracks with missing genres, and uses a locally running Ollama model to suggest appropriate genre tags.

The generated recommendations are intended to be **reviewed by the user before import**.

## Features

- Parses Rekordbox XML collections
- Detects tracks with missing genre metadata
- Uses a local Ollama LLM for genre inference
- Generates an Excel spreadsheet for manual review
- Produces an updated Rekordbox XML for import

## Output Files

- `rekordbox_genres.xlsx`
  - Suggested genre assignments
  - Intended for manual verification/editing

- `rekordbox_genres_updated.xml`
  - Updated Rekordbox collection with reviewed genre tags
  - Ready for import into Rekordbox

---

# Disclaimer

These tools are intended for personal music library management.

Users are responsible for ensuring they comply with all applicable copyright laws, platform terms of service, and licensing requirements in their jurisdiction.
