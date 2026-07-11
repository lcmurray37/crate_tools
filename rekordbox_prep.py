import os
import shutil
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

# --- CONFIGURATION ---
# The master directory where your Rekordbox-ready batch folders will live
MASTER_LIBRARY = Path.home() / "Music" / "Rekordbox_Library"

def process_file(file_path, dest_dir):
    supported = ('.mp3', '.wav', '.aif', '.aiff', '.flac', '.m4a')
    if file_path.suffix.lower() not in supported:
        return False
    
    dest_path = dest_dir / file_path.name
    
    # Duplicate Prevention: If file already exists, skip it
    if dest_path.exists():
        print(f"⚠️ Skipped (Duplicate): {file_path.name}")
        return False
        
    try:
        # Using copy2 to preserve original file creation/modification metadata
        shutil.copy2(str(file_path), str(dest_path))
        print(f"✅ Ingested: {file_path.name}")
        return True
    except Exception as e:
        print(f"❌ Error copying {file_path.name}: {e}")
        return False

def main():
    # Hide root Tkinter window
    root = tk.Tk()
    root.withdraw()
    
    print("Select the source folder containing your new music downloads...")
    source_dir = filedialog.askdirectory(title="Select Source Folder (Downloads/Rip Folder)")
    if not source_dir:
        print("Cancelled.")
        return
        
    source_path = Path(source_dir)
    
    # Create workflow tracking folder named by current date (YYYY-MM-DD)
    date_str = datetime.now().strftime("%Y-%m-%d")
    dest_dir = MASTER_LIBRARY / f"Import_{date_str}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nProcessing tracks into: {dest_dir}\n" + "-"*40)
    
    tracks_moved = 0
    # Recursively find and flatten all audio files into the date folder
    for root_dir, _, files in os.walk(source_path):
        for file in files:
            if process_file(Path(root_dir) / file, dest_dir):
                tracks_moved += 1
            
    print("-"*40)
    print(f"Finished! Successfully ingested {tracks_moved} tracks.")
    print(f"Ready for Rekordbox import here: {dest_dir}")

if __name__ == "__main__":
    main()