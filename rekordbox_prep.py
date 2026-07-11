import xml.etree.ElementTree as ET
import pandas as pd
from openai import OpenAI
import os
from concurrent.futures import ThreadPoolExecutor # For speed optimization

# --- CONFIGURATION ---
XML_INPUT_PATH = "rekordbox_collection.xml"  
EXCEL_OUTPUT_PATH = "missing_genres_suggestions.xlsx"
XML_OUTPUT_PATH = "rekordbox_genres_updated.xml"
MAX_WORKERS = 4  # Adjust based on your Mac (4 handles a MacBook Air well without choking it)

# Point to your local Ollama server (No API key required!)
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama-local-free" 
)

def parse_rekordbox_xml(xml_path):
    print("Parsing Rekordbox XML...")
    tree = ET.parse(xml_path)
    root = tree.getroot() # Simplified the Jupyter check out since this runs as a script
    
    collection = root.find('COLLECTION')
    missing_genre_tracks = []
    all_tracks_dict = {} 
    
    for track in collection.findall('TRACK'):
        track_attrib = track.attrib
        track_id = track_attrib.get('TrackID')
        genre = track_attrib.get('Genre', '').strip()
        
        all_tracks_dict[track_id] = track_attrib
        
        if not genre:
            missing_genre_tracks.append({
                'TrackID': track_id,
                'Name': track_attrib.get('Name'),
                'Artist': track_attrib.get('Artist'),
                'Album': track_attrib.get('Album'),
                'Original_Genre': genre
            })
            
    print(f"Found {len(missing_genre_tracks)} tracks missing a genre.")
    return missing_genre_tracks, tree, all_tracks_dict

def fetch_single_genre(track, index, total):
    """Worker function to process a single track"""
    prompt = f"Identify the primary electronic music/DJ genre for the following track:\nArtist: {track['Artist']}\nTitle: {track['Name']}\nAlbum: {track['Album']}\n\nRespond with ONLY the genre name (e.g., 'House', 'Techno', 'Drum & Bass', 'Tech House'). Max 3 words."
    
    try:
        response = client.chat.completions.create(
            model="gemma2:2b", 
            messages=[
                {"role": "system", "content": "You are an expert DJ and music archivist. You output only the exact genre string."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=10
        )
        suggested_genre = response.choices[0].message.content.strip().replace("'", "").replace('"', '')
        print(f"[{index}/{total}] {track['Artist']} - {track['Name']} -> {suggested_genre}")
    except Exception as e:
        print(f"Error fetching genre for {track['Name']}: {e}")
        suggested_genre = "Unknown"
        
    track['Suggested_Genre'] = suggested_genre
    return track

def get_llm_genre_suggestions_parallel(tracks):
    print(f"Consulting LLM for genre suggestions using {MAX_WORKERS} parallel workers...")
    total_tracks = len(tracks)
    
    # Use multi-threading to process tracks concurrently
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(fetch_single_genre, track, i + 1, total_tracks) for i, track in enumerate(tracks)]
        updated_tracks = [future.result() for future in futures]
        
    return updated_tracks

def generate_excel_and_xml(updated_tracks, tree, all_tracks_dict):
    df = pd.DataFrame(updated_tracks)
    df.to_excel(EXCEL_OUTPUT_PATH, index=False)
    print(f"Saved suggestions spreadsheet to: {EXCEL_OUTPUT_PATH}")
    
    root = tree.getroot()
    collection = root.find('COLLECTION')
    collection.clear()
    collection.attrib['Entries'] = str(len(updated_tracks))
    
    for track in updated_tracks:
        track_id = track['TrackID']
        orig_attribs = all_tracks_dict[track_id]
        orig_attribs['Genre'] = track['Suggested_Genre']
        
        new_track_element = ET.Element('TRACK', orig_attribs)
        collection.append(new_track_element)
        
    tree.write(XML_OUTPUT_PATH, encoding='utf-8', xml_declaration=True)
    print(f"Saved automated Rekordbox import XML to: {XML_OUTPUT_PATH}")

if __name__ == "__main__":
    if not os.path.exists(XML_INPUT_PATH):
        print(f"Error: Please export your Rekordbox collection as XML and save it as '{XML_INPUT_PATH}' in this folder.")
    else:
        missing_tracks, original_tree, full_dict = parse_rekordbox_xml(XML_INPUT_PATH)
        if missing_tracks:
            # TIP: For a quick test, change `missing_tracks` to `missing_tracks[:5]` below
            completed_tracks = get_llm_genre_suggestions_parallel(missing_tracks)
            generate_excel_and_xml(completed_tracks, original_tree, full_dict)
            print("\nDone! Follow the instructions to load these back into Rekordbox.")
        else:
            print("No tracks missing a genre found!")