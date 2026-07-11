import subprocess
import os
import tkinter as tk
from tkinter import filedialog

# Define your Spotify playlist and target export parameters
PLAYLIST_URL = "https://open.spotify.com/playlist/02CDUWMVArfbpKiamauSJw?si=afdeb43fe44d4287"
BITRATE = "320k"
AUDIO_FORMAT = "mp3"

def get_target_folder():
    """Opens a native OS folder selection dialog and returns the path."""
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder_selected = filedialog.askdirectory(title="Select Rekordbox Download Destination Folder")
    return folder_selected

def download_rekordbox_tracks():
    # 1. Trigger the folder chooser UI
    target_folder = get_target_folder()
    
    if not target_folder:
        print("❌ Operation cancelled: No destination folder selected.")
        return
        
    print(f"📁 Selected Destination: {target_folder}")
    print("\n🚀 Initiating playlist mirror sequence...")
    
    # 2. Executing spotDL command (Cleaned up flags)
    command = [
        "/Users/lmurray/gitprojects/myenv/bin/spotdl", "download", PLAYLIST_URL,
        "--format", AUDIO_FORMAT,
        "--bitrate", BITRATE
    ]
    
    try:
        # Run the subprocess inside the UI-selected directory
        subprocess.run(command, check=True, cwd=target_folder)
        print("\n✅ Sync complete! Tracks are formatted and ready for Rekordbox import.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Automation failed: {e}")

if __name__ == "__main__":
    download_rekordbox_tracks()