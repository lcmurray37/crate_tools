import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog

PLAYLIST_URL = "https://open.spotify.com/album/2viAtDQOMudvTXVAgsItKk?si=fh8GIP3eTOqDNmYJxboeew"
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


def download_tracks(spotdl_path, destination):
    """Run spotdl in the selected destination folder."""
    command = [
        spotdl_path,
        "download",
        PLAYLIST_URL,
        "--format",
        AUDIO_FORMAT,
        "--bitrate",
        BITRATE,
    ]

    subprocess.run(command, check=True, cwd=destination)


def main():
    try:
        spotdl = find_spotdl()

        destination = get_target_folder()

        if not destination:
            print("No destination selected. Exiting.")
            return

        print(f"Destination: {destination}")
        print("Starting download...\n")

        download_tracks(spotdl, destination)

        print("\nDownload complete!")

    except subprocess.CalledProcessError as e:
        print(f"\nspotdl exited with status {e.returncode}")

    except RuntimeError as e:
        print(f"\n{e}")


if __name__ == "__main__":
    main()