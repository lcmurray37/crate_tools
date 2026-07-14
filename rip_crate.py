import shutil
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

BITRATE = "320k"
AUDIO_FORMAT = "mp3"


def find_spotdl():
    """Locate the spotdl executable in the current environment."""
    spotdl = shutil.which("spotdl")

    if not spotdl:
        raise RuntimeError(
            "spotdl is not installed or is not on your PATH.\n"
            "Activate your virtual environment and run:\n"
            "pip install spotdl"
        )

    print(f"Using spotdl: {spotdl}")
    return spotdl


def get_playlist_url():
    """Get the Spotify URL from the command line or prompt the user."""
    if len(sys.argv) > 1:
        return sys.argv[1].strip()

    while True:
        url = input("Enter the Spotify playlist/album/track URL:\n> ").strip()

        if url:
            return url

        print("Please enter a valid URL.\n")


def get_target_folder():
    """Prompt the user to select a destination folder."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    folder = filedialog.askdirectory(
        title="Select Download Destination"
    )

    root.destroy()
    return folder


def download_tracks(spotdl_path, spotify_url, destination):
    """Run spotdl in the selected destination folder."""
    command = [
        spotdl_path,
        "download",
        spotify_url,
        "--format",
        AUDIO_FORMAT,
        "--bitrate",
        BITRATE,
    ]

    subprocess.run(command, check=True, cwd=destination)


def main():
    try:
        spotdl = find_spotdl()

        playlist_url = get_playlist_url()

        destination = get_target_folder()

        if not destination:
            print("No destination selected. Exiting.")
            return

        destination = Path(destination)

        print(f"\nDestination: {destination}")
        print("Starting download...\n")

        download_tracks(spotdl, playlist_url, destination)

        print("\nDownload complete!")
        print(f"Files saved to:\n{destination.resolve()}")

    except subprocess.CalledProcessError as e:
        print(f"\nspotdl exited with status {e.returncode}")

    except RuntimeError as e:
        print(f"\n{e}")


if __name__ == "__main__":
    main()